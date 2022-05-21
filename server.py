import os
from backend.api import api
from flask import Flask, send_from_directory

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

STATIC_FOLDER = os.path.join("frontend", "dist")

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static_files(path):
    path = os.path.join(STATIC_FOLDER, path)
    
    if os.path.isfile(path):
        directory, filename = os.path.split(path)
    else:
        directory = STATIC_FOLDER
        filename = "index.html"

    return send_from_directory(directory, filename)
