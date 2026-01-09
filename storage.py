import json
from pathlib import Path
from config import SOCKET_PATH
import socket

DATA_FILE = Path.home() / ".local/share/notifyd/notifications.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_notifications():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text())


def save_notifications(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(str(SOCKET_PATH))
    sock.send(b"reload")
