from flask import Flask, request, send_file
import os

app = Flask(__name__)

BASE_DIR = "documents"


@app.route("/download")
def download():
    filename = request.args.get("file", "")
    path = os.path.join(BASE_DIR, filename)
    return send_file(path)