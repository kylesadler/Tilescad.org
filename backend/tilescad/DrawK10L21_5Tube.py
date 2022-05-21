import scadnano as sc
from CoreTileTubeGeometry import CoreTileTubeGeometry
from CoreTileSpec import CoreTileSpec
from CoreTileTubeLayer import CoreTileTubeLayer
from genTubeAbstractTileSet import genTubeAbstractTileSet

def create2FullLayerK10_K6_alternating_verbose():
    tube_diam = 12
    num_unique_layers = 2
    num_reps = 2

    helices = [sc.Helix(max_offset=1024) for _ in range(tube_diam)]
    design = sc.Design(helices=helices, grid=sc.square)

    dom_len = 10
    core21_len = 21
    core22_len = 22

    ct_10_21_spec = CoreTileSpec(dom_len, 25, 6, 6, 25, dom_len)
    ct_10_22_spec = CoreTileSpec(dom_len, core22_len, dom_len, dom_len, core22_len, dom_len)

    ct_i10_o6_spec = CoreTileSpec(6, 25, 10, 10, 25, 6)
    ct_i6_o10_spec = CoreTileSpec(6, 26, 6, 6, 26, 6)

    tube_layers = [CoreTileTubeLayer([ct_10_21_spec]),
                   CoreTileTubeLayer([ct_10_22_spec]),
                   CoreTileTubeLayer([ct_i10_o6_spec]),
                   CoreTileTubeLayer([ct_i6_o10_spec])]

    ct_12helix_tube= CoreTileTubeGeometry(tube_diam, tube_layers, num_reps)

    ct_12helix_tube.draw(design)

    return design

def create2FullLayerK10_K6_alternating():
    tube_diam = 12
    num_unique_layers = 2
    num_reps = 5

    helices = [sc.Helix(max_offset=1024) for _ in range(tube_diam)]
    design = sc.Design(helices=helices, grid=sc.square)

    tube_layers = [CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(10, 10, 31)]),
                   CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(10, 6, 32)]),
                   CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(6, 6, 31)]),
                   CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(6, 10, 32)])]

    ct_12helix_tube = CoreTileTubeGeometry(tube_diam, tube_layers, num_reps)

    ct_12helix_tube.draw(design):

    return design

def create1FullLayerK10_verbose():
    tube_diam = 12
    num_unique_layers = 2
    num_reps = 2

    helices = [sc.Helix(max_offset=1024) for _ in range(tube_diam)]
    design = sc.Design(helices=helices, grid=sc.square)

    dom_len = 10
    core21_len = 21
    core22_len = 22

    ct_10_21_spec = CoreTileSpec(dom_len, core21_len, dom_len, dom_len, core21_len, dom_len)
    ct_10_22_spec = CoreTileSpec(dom_len, core22_len, dom_len, dom_len, core22_len, dom_len)

    tube_layers = [CoreTileTubeLayer([ct_10_21_spec]),
                   CoreTileTubeLayer([ct_10_22_spec])]

    ct_12helix_tube= CoreTileTubeGeometry(tube_diam, tube_layers, num_reps)

    ct_12helix_tube.draw(design)
    
    return design

def create1FullLayerK10():
    tube_diam = 12
    num_unique_layers = 2
    num_reps = 4

    helices = [sc.Helix(max_offset=1024) for _ in range(tube_diam)]
    design = sc.Design(helices=helices, grid=sc.square)

    tube_layers = [CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(10, 10, 31)]),
                   CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(10, 10, 32)])]

    ct_12helix_tube= CoreTileTubeGeometry(tube_diam, tube_layers, num_reps)

    ct_12helix_tube.draw(design)

    return design

def create1FullLayerK10_Abstract():
    tube_diam = 12
    num_reps = 1
    tile_set_name = 'k10'
    helices = [sc.Helix(max_offset=1024) for _ in range(tube_diam)]
    design = sc.Design(helices=helices, grid=sc.square)

    tube_layers = [CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(10, 10, 31)]),
                   CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(10, 10, 32)])]

    ab_ct_set = genTubeAbstractTileSet(12, 2, tile_set_name)
    ct_12helix_tube= CoreTileTubeGeometry(tube_diam, tube_layers, num_reps, ab_ct_set)

    ct_12helix_tube.draw(design)

    return design

def create2FullLayerK10_K6_alternating_Abstract():
    tube_diam = 12
    num_unique_layers = 2
    num_reps = 2

    helices = [sc.Helix(max_offset=1024) for _ in range(tube_diam)]
    design = sc.Design(helices=helices, grid=sc.square)

    tube_layers = [CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(10, 10, 31)]),
                   CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(10, 6, 32)]),
                   CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(6, 6, 31)]),
                   CoreTileTubeLayer([CoreTileSpec.byIO_CO_Lens(6, 10, 32)])]

    ab_ct_set = genTubeAbstractTileSet(12, 4)

    ct_12helix_tube = CoreTileTubeGeometry(tube_diam, tube_layers, num_reps, ab_ct_set)

    ct_12helix_tube.draw(design)

    return design

if __name__ == '__main__':
    #design = create2FullLayerK10_K6_alternating_verbose()
    #design = create2FullLayerK10_K6_alternating()
    #design = create1FullLayerK10_verbose()
    #design = create1FullLayerK10()
    design = create1FullLayerK10_Abstract()
    #design = create2FullLayerK10_K6_alternating_Abstract()
    design.write_scadnano_file()