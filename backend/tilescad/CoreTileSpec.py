class CoreTileSpec:
    # domain lengths for core tile
    """
    A class for storing information about the lengths (i.e. number of nucleotides) of domains of a core tile.

    ...

    Attributes
    __________
    ne_len : an int specifying the length of the northeast domain
    n_core_len : an int specifying the length of the north core domain
    nw_len : an int specifying the length of the northwest domain
    sw_len : an int specifying the length of the southwest domain
    s_core_len : an int specifying the length of the south core domain
    se_len : an int specifying the length of the southeast domain
    """
    def __init__(self, ne_len: int, n_core_len: int, nw_len: int,
                 sw_len: int, s_core_len: int, se_len: int):
        """

        :param ne_len: an int specifying the length of the northeast domain
        :param n_core_len: an int specifying the length of the north core domain
        :param nw_len: an int specifying the length of the northwest domain
        :param sw_len: an int specifying the length of the southwest domain
        :param s_core_len: an int specifying the length of the south core domain
        :param se_len: an int specifying the length of the southeast domain
        """
        self.ne_len = ne_len
        self.n_core_len = n_core_len
        self.nw_len = nw_len
        self.sw_len = sw_len
        self.s_core_len = s_core_len
        self.se_len = se_len

    @classmethod
    def byIO_CO_Lens(cls, input_len: int, output_len: int, alternating_co_spacing: int):
        """
        Specify the lengths of domains of a core tile by specifying the length of the input domains (i.e. sw and nw
        domains), the length of the output domains (i.e. se and ne domains), and the length of the alternate crossover
        spacing (i.e. the distance in nucleotides from the crossover of this tile to the crossover of the north and
        south tiles which bind to the outputs of this tile).

        :param input_len: an int specifying the length of the input domains (i.e. sw and nw domains)
        :param output_len: an int specifying the length of the output domains (i.e. se and ne domains)
        :param alternating_co_spacing: an int specifying the alternate crossover spacing (i.e. the distance in
        nucleotides from the crossover of this tile to the crossover of the north and
        south tiles which bind to the outputs of this tile)
        :return: CoreTileSpec
        """
        ne_len = output_len
        n_core_len = alternating_co_spacing - input_len
        nw_len = input_len
        sw_len = input_len
        s_core_len = alternating_co_spacing - input_len
        se_len = output_len

        return cls(ne_len, n_core_len, nw_len, sw_len, s_core_len, se_len)

    @classmethod
    def by_dom_aco_lens(cls, naco: int, saco: int, dom_len: int):
        """
        Specify the lengths of domains of a core tile by specifying the length of input domains and the north and south
        alternate crossover spacings (i.e. the distance in nucleotides from the crossover of this tile to the crossover
        of the north (south) tiles which bind to the outputs of this tile).
        :param naco: an int specifying the north alternate crossover spacing
        :param saco: an int specifying the south alternate crossover spacing
        :param dom_len: an int specifying the glue domain lengths
        :return: CoreTileSpec
        """

        # same as byIO_CO_Lens but with different north and south core lengths
        ne_len = dom_len
        n_core_len = naco-dom_len
        nw_len = dom_len
        sw_len = dom_len
        s_core_len = saco - dom_len
        se_len = dom_len

        return cls(ne_len, n_core_len, nw_len, sw_len, s_core_len, se_len)


    @classmethod
    def by_core_width(cls, core_width: int, domain_length: int):
        """
        Specify the lengths of domains of a core tile by specifying the length of input domains and the north and south
        alternate crossover spacings (i.e. the distance in nucleotides from the crossover of this tile to the crossover
        of the north (south) tiles which bind to the outputs of this tile).
        :param naco: an int specifying the north alternate crossover spacing
        :param saco: an int specifying the south alternate crossover spacing
        :param dom_len: an int specifying the glue domain lengths
        :return: CoreTileSpec
        """

        # same as byIO_CO_Lens but with different north and south core lengths
        ne_len = domain_length
        n_core_len = core_width
        nw_len = domain_length
        sw_len = domain_length
        s_core_len = core_width
        se_len = domain_length

        return cls(ne_len, n_core_len, nw_len, sw_len, s_core_len, se_len)
