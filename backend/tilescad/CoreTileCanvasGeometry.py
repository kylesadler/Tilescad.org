from collections import namedtuple
from .CoreTileMotif import CoreTileMotif
from .CoreTileTubeLayer import CoreTileTubeLayer
from .CoreTileSpec import CoreTileSpec
from .tiles.CoreTile import CoreTile
import scadnano as sc
from typing import List
from .CoreTileGeometry import CoreTileGeometry
from .get_tile_set_labels import get_tile_set_labels
from pprint import pprint

class CoreTileCanvasGeometry(CoreTileGeometry):
    """
    A class which generates a grid (i.e. list of lists) of CoreTileMotifs (which specifies dimensions for core tile
    domains, grid and helical positions for the 5' end of the tile, grid and helical positions for the 3' end of the
    tile, and domain labels if an CoreTile grid is passed) that form a canvas_size * canvas_size
    "square" canvas.  The elements of this grid are formed by
    first calculating the position of the origin tile (the at pos 0,0). Then filling out row 0 by
    calculating starting position offsets for tiles assuming the se glue of tile
    [0][j] (j \in [1,2,..., canvas_size -1]) binds to the ne glue of the tile at [0][j-1].
    A new row of tiles [i+1][0] begins with calculating the starting position of the tile at location [i+1][0] by
    assuming this tile attaches to the se glue of the tile at location [i][0].  The rest of this row is filled in
    using the previously described method of filling in rows.

    ...

    Attributes
    ----------
    grid : List[List[CoreTileMotif]]
        A 2D array of CoreTileMotif's which when drawn, form a canvas where each side is composed of
        canvas_size tiles stacked diagonally

    """

    def __init__(
        self,
        canvas_size: int,
        core_lengths,
        input_grid: List[List[CoreTileSpec]], # input data 
        tile_label_prefix: str = None,
    ):
        """
        Generates a grid of core tiles which forms a "square" canvas.  To add an element (i.e. CoreTileMotif) to
        a design, call the draw method of the element.

        :param canvas_size: side length (in number of "stacked" diagonal tiles) of canvas
        :param input_grid: A list of CoreTileTubeLayers (which themselves are a list of CoreTileSpec's). The jth core
        tile in the ith column of grid will have core tile dimensions input_grid[i%input_grid.len].get_lengths(j).
        :param ab_ct_tile_set: Optional (default=None) 2D array of AbstractCoreTiles used to specify domain names
        for the tiles in the canvas.
        """

        # pass in what each tile should look like

        tile_set_labels = None if tile_label_prefix is None else get_tile_set_labels(canvas_size, tile_label_prefix)

        # if self._tile_set_not_valid(tile_set_labels, canvas_size):
        #     raise ValueError("Abstract tile set not compatible with tube geometry")

        # grid[i][j] should be jth column, ith row
        self.grid = []

        # left to right, bottom to top
        # (north west to south east, south west to north east)
        for i in range(canvas_size):
            row = []
            for j in range(canvas_size):
                lengths = input_grid[i][j]
                if lengths is None:
                    row.append(None)
                    continue
                labels = None if tile_set_labels is None else tile_set_labels[i][j]

                if j == 0 and i == 0:
                    start_pos = lengths.nw_len + lengths.n_core_len + lengths.ne_len
                    row.append(CoreTileMotif(lengths, canvas_size - 1, canvas_size, start_pos, labels))
                    continue
                
                start_helix = None
                end_helix = None
                start_pos = None

                if j != 0 and row[j - 1] is not None:
                    # if there is a tile to our left (north west)
                    se_dom = row[j - 1].se_dom_seg
                    start_helix = se_dom.helix
                    end_helix = se_dom.helix + 1
                    # 5p is the start
                    start_pos = se_dom.offset_5p() + lengths.nw_len + lengths.n_core_len + lengths.ne_len
                
                if i != 0 and self.grid[i - 1][j] is not None:
                    # if there is a tile below us (south west), make sure it gives the same constraints
                    # as the left (north west) tile
                    ne_dom = self.grid[i - 1][j].ne_dom_seg

                    # print(start_helix, ne_dom.helix)
                    assert start_helix is None or start_helix == ne_dom.helix - 1
                    start_helix = ne_dom.helix - 1

                    assert end_helix is None or end_helix == ne_dom.helix
                    end_helix = ne_dom.helix

                    # 3p is the end
                    new_start_pos = ne_dom.offset_3p() + lengths.nw_len + lengths.n_core_len + lengths.ne_len
                    # print(start_pos, new_start_pos)
                    assert start_pos is None or start_pos == new_start_pos
                    start_pos = new_start_pos
                        

                # TODO make a general solution for this
                if start_helix is None or end_helix is None or start_pos is None:
                    start_helix = canvas_size - 1 + j - i
                    end_helix = start_helix + 1

                    # lengths.nw_len + lengths.n_core_len + lengths.ne_len
                    start_pos = sum([core_lengths[x] or 0 for x in range(i + j + 1)]) + (lengths.ne_len) * (i + j + 1) + lengths.nw_len


                
                row.append(CoreTileMotif(lengths, start_helix, end_helix, start_pos, labels))

            self.grid.append(row)

    def _tile_set_not_valid(ct_set: List[List[CoreTile]], canvas_size):
        """
        This checks to ensure that no abstract core tile appears more than once in ab_ct_tile_set.  This is due
        to the fact that an abstract core tile appearing more than once could be assigned to two core tile motifs
        with different domain dimensions which would mean that two of the same glues could map to potentially
        different sequences (we don't want this!).  Returns True if the tile set contains duplicate tiles and false
        otherwise.

        :param ct_set: A 2D array of CoreTile's
        :param canvas_size: dimension of the canvas to form with ct_set
        :return: Boolean indicating whether the abstract tile set is valid or not
        """
        # TODO: Check wether ct_set is compatible with canvas_size
        # TODO: check to see if there are any duplicate tiles, we don't
        # want the same tile assigned to two different motifs
        # TODO: We want to modify this method so that it actually checks that
        # no glue is mapped onto two domains with different lengths
        # (i.e. number of nucleotides that compose the domain).
        return False
