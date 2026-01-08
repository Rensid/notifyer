import json
from pathlib import Path

DATA_FILE = Path.home() / ".local/share/notifyd/notifications.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_notifications():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text())


def save_notifications(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))
