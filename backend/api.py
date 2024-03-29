import sys
import traceback
from pprint import pprint
from .tilescad.DrawCanvasDebug import draw_flattish_canvas
from .tilescad.CoreTileSpec import CoreTileSpec
from flask import Blueprint, send_from_directory, request
from .util import get_current_time_ms, mkdir

api = Blueprint('api', __name__)

TEMP_DIRECTORY = "temp"


@api.route('/')
def index():
    return "called api!"


@api.route('/upload-design', methods=['POST'])
def upload_design():

    try:
        data = request.get_json()
        
        if(data is None):
            return "Data is missing", 400

        grid = data.get("grid", None)
        domain_length = data.get("domainLength", None)
        tile_types = data.get("tileTypes", None)

        if(grid is None or domain_length is None or tile_types is None):
            return "Data is missing", 400

        if(not isinstance(grid, list) or not isinstance(grid[0], list) or len(grid) != len(grid[0])):
            return "Invalid data", 400

        if(domain_length > 30 or len(grid) > 60 or len(tile_types) > 50):
            return "Invalid data", 400

        canvas_dim = len(grid)
        # pprint(grid)

        # naco = north alternating crossover spacing
        # saco = south alternating crossover spacing

        core_lengths = [None]* (canvas_dim + canvas_dim + 1)
        tile_grid = []
        for i in range(canvas_dim):
            row = []
            for j in range(canvas_dim):
                # traverse list of rows backwards so image is flipped appropriately
                tile_id = grid[len(grid)-i-1][j]
                tile = {} if tile_id is None else tile_types[tile_id]
                core_width = tile.get("coreLength", None)
                if core_width is not None:
                    if core_lengths[i+j] is None:
                        core_lengths[i+j] = core_width
                    elif core_lengths[i+j] != core_width:
                        return "Invalid data", 400
                    row.append(CoreTileSpec.by_core_width(core_width, domain_length))
                else:
                    row.append(None)

            tile_grid.append(row)

        design = draw_flattish_canvas(tile_grid, canvas_dim, core_lengths, None)
        filename = f'canvas_design_{round(get_current_time_ms()*10000)}.json'
        design.write_scadnano_file(directory=TEMP_DIRECTORY, filename=filename)

        return filename
    except Exception:
        print(traceback.format_exc())
        return "Server Error", 500



@api.route('/download-file', methods=['POST'])
def download_file():
    filename = request.form['filename']

    return send_from_directory(TEMP_DIRECTORY, path=filename, as_attachment=True)