import requests
import os
import json
import time
import shutil

# Cargar config
with open("config.json") as f:
    config = json.load(f)

NODE_NAME = config["node_name"]
PEERS = config["peers"]  # ahora es un dict: {url: nombre}

BACKUP_FOLDER = "backups"
RESTORE_FOLDER = "restored_nodes"

os.makedirs(RESTORE_FOLDER, exist_ok=True)

def is_alive(url):
    try:
        response = requests.get(f"{url}/ping", timeout=3)
        return response.status_code == 200
    except:
        return False

while True:
    print(f"[{NODE_NAME}] Verificando nodos vecinos...")

    for peer_url, peer_name in PEERS.items():
        alive = is_alive(peer_url)

        if not alive:
            print(f"[{NODE_NAME}] {peer_url} no responde. Restaurando respaldo de {peer_name}...")

            # Restaurar archivos de ese nodo desde backup
            source_dir = os.path.join(BACKUP_FOLDER, peer_name)
            dest_dir = os.path.join(RESTORE_FOLDER, peer_name)

            if os.path.exists(source_dir):
                os.makedirs(dest_dir, exist_ok=True)
                for file in os.listdir(source_dir):
                    src_file = os.path.join(source_dir, file)
                    dst_file = os.path.join(dest_dir, file)
                    shutil.copy2(src_file, dst_file)
                    print(f"  → Restaurado: {file}")
            else:
                print(f"  ⚠️ No hay respaldo local de {peer_name}")
    
    time.sleep(60)


