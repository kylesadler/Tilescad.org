import scadnano as sc
from .CoreTileCanvasGeometry import CoreTileCanvasGeometry
from .CoreTileSpec import CoreTileSpec
from .CoreTileTubeLayer import CoreTileTubeLayer
from .get_tile_set_labels import get_tile_set_labels


# this is what we're calling in the API
def draw_flattish_canvas(grid: list, canvas_dim: int, core_lengths, tile_label_prefix: str):
    # this function returns a sc.Design object with helices, strands, domains (possibly with names)

    # TODO: calculate the max_offset using canvas dim instead of hardcoding it with a fixed value

    # create canvas_dim x 2 helices because "up" is northeast and "side" is southeast
    # these are the grid rows that go down the page by default
    helices = [sc.Helix(max_offset=1024) for _ in range(canvas_dim * 2)]

    design = sc.Design(helices=helices, grid=sc.square)

    ct_16x16_k10_canvas = CoreTileCanvasGeometry(
        canvas_dim,
        core_lengths,
        grid,
        tile_label_prefix,
    )

    ct_16x16_k10_canvas.draw(design)

    return design


if __name__ == "__main__":
    k_len = 6
    canvas_dim = 16
    design = draw_flattish_canvas(k_len, canvas_dim, f"k{k_len}")
    filename = f"k{k_len}_canvas_dim{canvas_dim}.sc"
    design.write_scadnano_file(filename=filename)
