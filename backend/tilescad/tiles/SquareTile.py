class SquareTile:
    # labels
    """
    Represents a single abstract (45 degree rotated) square (diamond) tile defined by the glue labels on edges.
    Does not yet support glue strengths.

    ...

    Attributes
    ----------
    name : str
        name of tile
    ne_glue : str
        the label for the northeast glue
    nw_glue : str
        the label for the northwest glue
    sw_glue : str
        the label for the southwest glue
    se_glue : str
        the label for the southeast glue
    """
    def __init__(self, name: str, ne_glue: str, nw_glue: str, sw_glue: str, se_glue: str):
        self.name = name
        self.ne_glue = ne_glue
        self.nw_glue = nw_glue
        self.sw_glue = sw_glue
        self.se_glue = se_glue
