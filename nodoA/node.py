from flask import Flask, request
import os
import json

app = Flask(__name__)
BACKUP_FOLDER = "backups"

@app.route('/upload', methods=['POST'])
def upload():
    node_from = request.form['node']
    filename = request.form['filename']
    file = request.files['file']

    node_dir = os.path.join(BACKUP_FOLDER, node_from)
    os.makedirs(node_dir, exist_ok=True)

    filepath = os.path.join(node_dir, filename)
    file.save(filepath)

    return "OK", 200

@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

if __name__ == '__main__':
    with open("config.json") as f:
        config = json.load(f)
    app.run(host="0.0.0.0", port=config["port"])
