import os
import time
import json
import hashlib
import requests

WATCH_FOLDER = "my_files"
HASH_FILE = "file_hashes.json"

# Cargar configuración
with open("config.json") as f:
    config = json.load(f)

NODE_NAME = config["node_name"]
PEERS = config["peers"]

# Obtener hash SHA256 de un archivo
def hash_file(filepath):
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

# Cargar hashes previos (si existen)
if os.path.exists(HASH_FILE):
    with open(HASH_FILE, "r") as f:
        known_hashes = json.load(f)
else:
    known_hashes = {}

# Loop principal
while True:
    for filename in os.listdir(WATCH_FOLDER):
        filepath = os.path.join(WATCH_FOLDER, filename)
        if os.path.isfile(filepath):
            file_hash = hash_file(filepath)

            if filename not in known_hashes or known_hashes[filename] != file_hash:
                print(f"[{NODE_NAME}] Cambio detectado en {filename}, enviando respaldo...")

                for peer in PEERS:
                    try:
                        with open(filepath, "rb") as f:
                            response = requests.post(
                                f"{peer}/upload",
                                files={"file": f},
                                data={"node": NODE_NAME, "filename": filename},
                                timeout=5
                            )
                            print(f"[{NODE_NAME}] Enviado a {peer}: {response.status_code}")
                    except Exception as e:
                        print(f"[{NODE_NAME}] Error enviando a {peer}: {e}")

                # Actualizar hash local
                known_hashes[filename] = file_hash

    # Guardar el estado actual de los hashes
    with open(HASH_FILE, "w") as f:
        json.dump(known_hashes, f, indent=2)

    time.sleep(30)  # Esperar 30 segundos antes de revisar de nuevo
