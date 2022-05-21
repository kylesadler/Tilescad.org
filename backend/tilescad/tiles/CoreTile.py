from .SquareTile import SquareTile
from .Utils import domCom

class CoreTile(SquareTile):
    # labels for core tile
    """
        Represents a single abstract core tile defined by the glue labels on edges (given by an SquareTile)
        and domain labels for cores.Does not yet support glue strengths.

        ...

        Attributes
        ----------
        name : str
            name of tile
        ne_glue : str
            the label for the northeast glue
        n_core_glue : str
            the label for the domain on the tile to which the north core strand binds
        nw_glue : str
            the label for the northwest glue
        sw_glue : str
            the label for the southwest glue
        s_core_glue : str
            the label for the domain on the tile to which the south core strand binds
        se_glue : str
            the label for the southeast glue
        """
    def __init__(self, name: str, ne_glue: str, nw_glue: str, sw_glue: str, se_glue: str, n_core_dom: str, s_core_dom: str):
        """
        Parameters
        __________
        :param str n_core_dom:
            The label for the domain on the tile to which the north core strand binds
        :param str s_core_dom:
            The label for the domain on the tile to which the south core strand binds
        """
        super().__init__(name, ne_glue, nw_glue, sw_glue, se_glue)

        self.n_core_glue = n_core_dom
        self.s_core_glue = s_core_dom

        # these are the "external" strands that make core tile more solid
        self.n_core_strand_glue = domCom(self.n_core_glue)
        self.s_core_strand_glue = domCom(self.s_core_glue)