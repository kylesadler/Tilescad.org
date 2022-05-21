import scadnano as sc
from .CoreTileSpec import CoreTileSpec
from .tiles.CoreTile import CoreTile


class CoreTileMotif:
    # core tile but in Scadnano

    """
    A class which completely specifies an instance of a core tile in a Scadnano diagram.

    Attributes
    __________
    ne_len : an int specifying the length of the northeast domain
    n_core_len : an int specifying the length of the north core domain
    nw_len : an int specifying the length of the northwest domain
    sw_len : an int specifying the length of the southwest domain
    s_core_len : an int specifying the length of the south core domain
    se_len : an int specifying the length of the southeast domain

    ne_dom_seg : A scadnano domain specifying the tile's northeast glue
    n_core_tile_dom_seg : A scadnano domain specifying the tile's north core domain
    n_core_strand_dom : A scadnano domain specifying the domain for the north core strand
    nw_dom_seg : A scadnano domain specifying the tile's northwest domain
    sw_dom_seg : A scadnano domain specifying the tile's southwest domain
    s_core_tile_dom_seg : A scadnano domain specifying the tile's south core domain
    s_core_strand_dom  : A scadnano domain specifying the domain for the south core strand
    se_dom_seg : A scadnano domain specifying the tile's southeast domain

    tile_strand : A scadnano strand specifying the tile strand
    n_core_strand : A scadnano strand specifying the north core strand
    s_core_strand : A scadnano strand specifying the south core strand
    """

    def __init__(
        self,
        ct_spec: CoreTileSpec,
        start_helix: int,
        end_helix: int,
        start_pos: int,
        ab_ct: CoreTile = None,
    ):
        """
        Create a core tile which includes information about it's position in the scadnao helical grid and domain names

        :param ct_spec: A CoreTileSpec containing information about domain lengths
        :param start_helix: Helix which contains 5' end of tile
        :param end_helix: Helix which conatins 3' end of tile
        :param start_pos: Grid position on the start_helix on which to place the 5' end of the tile
        :param ab_ct: An optional (default=None) CoreTile used to specify domain names on the tile
        """

        assert start_helix is not None and end_helix is not None and start_pos is not None 

        # Define domain and tile names
        self.name = None
        self.ne_name = None
        self.n_core_tile_name = None
        self.n_core_strand_name = None
        self.nw_name = None
        self.sw_name = None
        self.s_core_tile_name = None
        self.s_core_strand_name = None
        self.se_name = None

        if ab_ct:
            self.name = ab_ct.name
            self.ne_name = ab_ct.ne_glue
            self.n_core_tile_name = ab_ct.n_core_glue
            self.n_core_strand_name = ab_ct.n_core_strand_glue
            self.nw_name = ab_ct.nw_glue
            self.sw_name = ab_ct.sw_glue
            self.s_core_tile_name = ab_ct.s_core_glue
            self.s_core_strand_name = ab_ct.s_core_strand_glue
            self.se_name = ab_ct.se_glue

        #######Define lengths##########
        self.ne_len = ct_spec.ne_len
        self.n_core_len = ct_spec.n_core_len
        self.nw_len = ct_spec.nw_len
        self.sw_len = ct_spec.sw_len
        self.s_core_len = ct_spec.s_core_len
        self.se_len = ct_spec.se_len

        ################Define domains###############
        curr_pos = start_pos

        self.ne_dom_seg = sc.Domain(
            start_helix, False, curr_pos - self.ne_len, curr_pos, name=self.ne_name
        )
        curr_pos = curr_pos - self.ne_len


        if self.n_core_len > 0:
            self.n_core_tile_dom_seg = sc.Domain(
                start_helix,
                False,
                curr_pos - self.n_core_len,
                curr_pos,
                name=self.n_core_tile_name,
            )

            # "external" strand
            self.n_core_strand_dom = sc.Domain(
                start_helix,
                True,
                curr_pos - self.n_core_len,
                curr_pos,
                name=self.n_core_strand_name,
            )
            curr_pos = curr_pos - self.n_core_len

        self.nw_dom_seg = sc.Domain(
            start_helix, False, curr_pos - self.nw_len, curr_pos, name=self.nw_name
        )
        curr_pos = curr_pos - self.nw_len

        self.sw_dom_seg = sc.Domain(
            end_helix, True, curr_pos, curr_pos + self.sw_len, name=self.sw_name
        )
        curr_pos = curr_pos + self.sw_len

        if self.s_core_len > 0:
            self.s_core_tile_dom_seg = sc.Domain(
                end_helix,
                True,
                curr_pos,
                curr_pos + self.s_core_len,
                name=self.s_core_tile_name,
            )
            # "external" strand
            self.s_core_strand_dom = sc.Domain(
                end_helix,
                False,
                curr_pos,
                curr_pos + self.s_core_len,
                name=self.s_core_strand_name,
            )
            curr_pos = curr_pos + self.s_core_len

        self.se_dom_seg = sc.Domain(
            end_helix, True, curr_pos, curr_pos + self.se_len, name=self.se_name
        )
        curr_pos = curr_pos + self.se_len

        ################Define Strands##################
        if self.n_core_len > 0 and self.s_core_len > 0:
            self.tile_strand = sc.Strand(
                [
                    self.ne_dom_seg,
                    self.n_core_tile_dom_seg,
                    self.nw_dom_seg,
                    self.sw_dom_seg,
                    self.s_core_tile_dom_seg,
                    self.se_dom_seg,
                ],
                label="tile",
                name=self.name,
            )
        else:
            self.tile_strand = sc.Strand(
                [
                    self.ne_dom_seg,
                    self.nw_dom_seg,
                    self.sw_dom_seg,
                    self.se_dom_seg,
                ],
                label="tile",
                name=self.name,
            )


        # "external" strands
        if self.n_core_len > 0:
            self.n_core_strand = sc.Strand(
                [self.n_core_strand_dom], label="n_core", name=self.n_core_strand_name
            )

        if self.s_core_len > 0:
            self.s_core_strand = sc.Strand(
                [self.s_core_strand_dom], label="s_core", name=self.s_core_strand_name
            )

    def se_binding_offset(self):
        """

        :return: int giving sw_len + s_core_len
        """
        return self.sw_len + self.s_core_len

    def side_lin(self):
        """

        :return: int giving nw_len + n_core_len + ne_len
        """
        return self.nw_len + self.n_core_len + self.ne_len

    def draw(self, design: sc.Design):
        """
        Draw the tile using start_helix, end_helix, start_pos on the passed design.

        :param design: A Scadnano Design on which to draw the tile
        :return: None
        """
        design.add_strand(self.tile_strand)

        # top and bottom tile caps
        if self.n_core_len > 0:
            design.add_strand(self.n_core_strand)

        if self.s_core_len > 0:
            design.add_strand(self.s_core_strand)
