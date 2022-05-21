from CoreTile import CoreTile

def genTubeAbstractTileSet(tube_diam: int, num_unique_half_layers: int, tile_set_label: str = None):
    """
        Generates an abstract tile set (as a 2D list) which in the aTAM would form a tube with tube_diam helices
         (if tiles ran along two helices like SSTs) and num_unique_half_layers number of layers.

        ...

        Attributes
        __________
        grid : A 2D list of CoreTile's which form a tube with tube_diam helices
        (if tiles ran along two helices like SSTs) and
        num_unique_half_layers number of layers.
        tube_diam: an int specifying the desired number of helices of tube
        num_unique_half_layers: an int specifying the number of unique half layers the tube should contain
    """

    """
    Generates an abstract tile set (as a 2D list) which in the aTAM would form a tube with tube_diam helices
        (if tiles ran along two helices like SSTs) and num_unique_half_layers number of layers.

    :param tube_diam: an int specifying the desired number of helices of tube
    :param num_unique_half_layers: an int specifying the number of unique half layers the tube should contain
    :param tile_set_label: Label to append to glues; useful for distinguishing glues on different tile sets during
    sequence design.  Default=None
    """
    if tube_diam % 2:
        raise ValueError('Tube diameter must be even')

    if num_unique_half_layers % 2:
        raise ValueError('Number of unique half layers must be even')

    grid_diam = int(tube_diam / 2)
    grid = [[None for h in range(grid_diam)] for l in range(num_unique_half_layers)]

    ga = ''
    if tile_set_label:
        ga = tile_set_label + '_'

    for i in range(num_unique_half_layers):
        for j in range(grid_diam):
            ofst = i % 2

            # not sure what these do
            var1 = (i + 1) % num_unique_half_layers
            var2 = (ofst + (j * 2) + 1) % tube_diam
            var3 = ofst + (j * 2)

            options = {
                "name" : f'Tile_{ga}{i}_{j}',
                "ne_glue" : f'g_{ga}{var1}_{var3}',
                "nw_glue" : f'g_{ga}{i}_{var3}*',
                "sw_glue" : f'g_{ga}{i}_{var2}*',
                "se_glue" : f'g_{ga}{var1}_{var2}',

                "n_core_dom" : f'n_core_{ga}{i}_{j}',
                "s_core_dom" : f's_core_{ga}{i}_{j}'
            }
            grid[i][j] = CoreTile(**options)

    return grid