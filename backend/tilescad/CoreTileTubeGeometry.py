from collections import namedtuple
from CoreTileMotif import CoreTileMotif
from CoreTileTubeLayer import CoreTileTubeLayer
from CoreTileSpec import CoreTileSpec
from CoreTile import CoreTile
import scadnano as sc
from typing import List
from CoreTileGeometry import CoreTileGeometry


class CoreTileTubeGeometry(CoreTileGeometry):
    """
    A class which generates a grid (i.e. list of lists) of CoreTileMotifs (which specifies dimensions for core tile
    domains, grid and helical positions for the 5' end of the tile, grid and helical positions for the 3' end of the
    tile, and domain labels if an CoreTile grid is passed) which form a tube-diam helix nanotube.  The
    last tile in each column wraps around so that it's southern domains are adjacent to the northern domains of the
    first tile.  This class assumes the tube is periodic and the num_reps argument controls the number of times
    the layers repeat.  Important note: We refer to a column of tiles which all have the same start position
    on some helix as a half-layer.

    ...

    Attributes
    ----------
    grid : List[List[CoreTileMotif]]
        A 2D array of CoreTileMotif's which when drawn, form a canvas where each side is composed of
        canvas_tile_dim tiles stacked diagonally
    tube_diam: int
        Number of helices the nanotube has
    tube_half_layers: List[CoreTileTubeLayer]
        A list of CoreTileTubeLayers (which themselves are a list of CoreTileSpec's).
    num_reps: The number of times to repeat layers in the grid
    """

    def __init__(
        self,
        tube_diam: int,
        tube_half_layers: List[CoreTileTubeLayer],
        num_reps: int,
        ab_ct_tile_set: List[List[CoreTile]] = None,
    ):
        """
        Generates a grid of core tiles which forms a nanotube with tube_diam helices.  To add an element
        (i.e. CoreTileMotif) to a design, call the draw method of the element.

        :param tube_diam: Number of helices desired in nanotube. Geometry constraints stemming from the geometry
        of a nanotube requires this be even.
        :param tube_half_layers: A list of CoreTileTubeLayer's.  For each desired unique half-layer, an element must be
        added to this list.  Geometry constraints stemming from the geometry of a nanotube requires this list must
        have an even number of elements.  The CoreTileSpec's contained in a CoreTileTubeLayer are periodically applied
        to the CoreTileMotifs along a column.  That is, he jth core tile in the ith column of grid will have
        core tile dimensions x_slices[i%x_slices.len].get_lengths(j).
        :param num_reps: The number of times to repeat unique half-layers.
        :param ab_ct_tile_set: An optional (default=None) 2D list of CoreTile's used for specifying domain
        names.  If passed, the length of this list must be equal to the length of tube_half_layers (since the number
        of elements in tube_half_layers specifies the number of unique half-layers).  The length of each list contained
        in ab_ct_tile_set
        """

        if tube_diam % 2:
            raise ValueError("Tube diameter must be even")

        self.tube_diam = tube_diam

        num_unique_layers = len(tube_half_layers)
        if num_unique_layers % 2:
            raise ValueError("Number of unique layers must be even")

        if ab_ct_tile_set and self._tile_set_not_valid(
            ab_ct_tile_set, tube_diam, tube_half_layers
        ):
            raise ValueError("Abstract tile set not compatible with tube geometry")

        tube_len = num_unique_layers * num_reps
        grid_diam = int(tube_diam / 2)
        self.grid = [[None for h in range(grid_diam)] for l in range(tube_len)]
        # grid[i][j] is the ith tile in the jth row

        core_lens = [21, 22]  # TODO: needed?
        dom_len = 10  # TODO: needed?

        for j in range(grid_diam):
            ab_ct = None
            if ab_ct_tile_set:
                ab_ct = ab_ct_tile_set[0][j]
                # print(ab_ct.name)
            self.grid[0][j] = self._createInitGridPos(
                tube_half_layers[0].get_lengths(j), j * 2, (j * 2) + 1, ab_ct
            )

        for i in range(1, tube_len):
            for j in range(grid_diam):
                ab_ct = None
                if ab_ct_tile_set:
                    ab_ct = ab_ct_tile_set[i % num_unique_layers][j]
                    # print(ab_ct.name)
                if i % 2 == 0:
                    self.grid[i][j] = self._createGridPosFromExistingNEdom(
                        tube_half_layers[i % num_unique_layers].get_lengths(j),
                        self.grid[i - 1][j].ne_dom_seg,
                        ab_ct,
                    )
                if i % 2 == 1:
                    self.grid[i][j] = self._createGridPosFromExistingSEdom(
                        tube_half_layers[i % num_unique_layers].get_lengths(j),
                        self.grid[i - 1][j].se_dom_seg,
                        ab_ct,
                    )

    @staticmethod
    def _tile_set_not_valid(
        ct_set: List[List[CoreTile]],
        tube_diam: int,
        tube_layers: List[CoreTileTubeLayer],
    ):
        """
        Checks to ensure the constraints regarding ab_ct_tile_set mentioned in the docs for __init__ arguments are
        satisfied.
        :param ct_set: A 2D list of CoreTile's
        :param tube_diam: Number of helices desired in nanotube.
        :param tube_layers: A list of CoreTileTubeLayer's
        :return: False if ct_set meets all constraints, True otherwise.
        """
        # The number of half layers in the tile set must be the same as the number of tube layers
        if len(ct_set) != len(tube_layers):
            print("tube layers differ")
            return True
        # The abstract tile set should have the same "diameter" as the tube on which it's being applied
        for col in ct_set:
            if len(col) != int(tube_diam / 2):
                print("tube diams differ")
                return True

        # TODO: check no tile is repeated in abstract tile set

        return False

    def _createInitGridPos(
        self,
        spec: CoreTileSpec,
        start_helix: int,
        end_helix: int,
        ab_ct: CoreTile = None,
    ):
        """
        Generates a CoreTileMotif with the 5' end on the start helix, the 3' end on the end helix, the crossover
        at position 0 and names domains based on the glues of ab_ct (if passed).

        :param spec: A CoreTileSpec which specifies the domain lengths to use for generating the CoreTileMotif
        :param start_helix: An integer specifying the helix on which to place the 5' end of the core tile
        :param end_helix: An integer specifying the helix on which to place the 3' end of the core tile
        :param ab_ct: An optional (default = None) CoreTile; it's glues are used to name domains
        :return: CoreTileMotif
        """
        #######Define lengths##########
        ne_len = spec.ne_len
        n_core_len = spec.n_core_len
        nw_len = spec.nw_len

        side_lin = nw_len + n_core_len + ne_len

        return CoreTileMotif(spec, start_helix, end_helix, side_lin, ab_ct)

    def _createGridPosFromExistingSEdom(
        self, spec: CoreTileSpec, se_dom: sc.Domain, ab_ct: CoreTile = None
    ):
        """
        Generates a CoreTileMotif so that it's nw domain is adjacent to se_dom

        :param spec: A CoreTileSpec which specifies the domain lengths to use for generating the CoreTileMotif
        :param se_dom: The southeast domain of an existing CoreTileMotif
        :param ab_ct: An optional (default = None) CoreTile; it's glues are used to name domains
        :return: CoreTileMotif
        """

        nw_len = spec.nw_len
        n_core_len = spec.n_core_len
        ne_len = spec.ne_len

        start_pos = se_dom.offset_5p() + nw_len + n_core_len + ne_len
        start_helix = se_dom.helix
        end_helix = (se_dom.helix + 1) % self.tube_diam

        return CoreTileMotif(spec, start_helix, end_helix, start_pos, ab_ct)

    def _createGridPosFromExistingNEdom(
        self, spec: CoreTileSpec, ne_dom: sc.Domain, ab_ct: CoreTile = None
    ):
        """
        Generates a CoreTileMotif so that it's sw domain is adjacent to ne_dom

        :param spec: A CoreTileSpec which specifies the domain lengths to use for generating the CoreTileMotif
        :param ne_dom: The northeast domain of an existing CoreTileMotif
        :param ab_ct: An optional (default = None) CoreTile; it's glues are used to name domains
        :return: CoreTileMotif
        """

        nw_len = spec.nw_len
        n_core_len = spec.n_core_len
        ne_len = spec.ne_len

        start_helix = (ne_dom.helix - 1) % self.tube_diam
        end_helix = ne_dom.helix

        start_pos = ne_dom.offset_3p() + nw_len + n_core_len + ne_len

        return CoreTileMotif(spec, start_helix, end_helix, start_pos, ab_ct)
