from .CoreTileSpec import CoreTileSpec
from typing import List


class CoreTileTubeLayer:
    """
    A class used for specifying the domain dimensions of layers of (periodically repeating) core tiles.

    ...

    Attributes
    __________
    layer : list of CoreTileSpec's

    """

    def __init__(self, layer: List[CoreTileSpec]):
        """

        :param layer: List[CoreTileSpec]
        """
        self.layer = layer

    def get_lengths(self, i: int):
        """
        Returns the ith element of the infinitely repeating layer list
        :param i: an int
        :return: CoreTileSpec
        """
        return self.layer[i % len(self.layer)]
