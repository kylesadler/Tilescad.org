from .tiles.CoreTile import CoreTile

def get_tile_set_labels(canvas_dim: int, tile_set_label: str = None):
    """
    Generates an abstract tile set (as a 2D list) which in the aTAM would form a hardcoded canvas_dim*canvas_dim
    square (with no repeated glues; other than on abutting glues).

    ...

    returns
    __________
    grid : A 2D list of CoreTile's which form a "hardcoded" square in the aTAM

    :param canvas_dim: Desired side length (i.e. number of tiles) of square canvas.
    :param tile_set_label: Label to append to glues; useful for distinguishing glues on different tile sets during
    sequence design.  Default=None
    """
    grid = [[None for h in range(canvas_dim)] for l in range(canvas_dim)]

    prefix = tile_set_label + '_' if tile_set_label else ''

    for i in range(canvas_dim):
        for j in range(canvas_dim):
            options = {
                "name" : f'Tile_{prefix}{i}_{j}',
                "ne_glue" : f'ne_{prefix}{i+1}_{j+1}',
                "nw_glue" : f'nw_{prefix}{i+1}_{j}*',
                "sw_glue" : f'sw_{prefix}{i}_{j+1}*',
                "se_glue" : f'se_{prefix}{i+1}_{j+1}',

                "n_core_dom" : f'n_core_{prefix}{i}_{j}',
                "s_core_dom" : f's_core_{prefix}{i}_{j}'
            }
            grid[i][j] = CoreTile(**options)

    return grid