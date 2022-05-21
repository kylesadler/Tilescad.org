class CoreTileGeometry:
    def draw(self, design):
        for tile_row in self.grid:
            for tile in tile_row:
                if tile is not None:
                    tile.draw(design)
