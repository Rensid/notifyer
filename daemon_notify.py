import json
import time
from enum import Enum
from functools import partial
from pathlib import Path
from threading import Lock
import socket

import schedule
from notifypy import Notify

from storage import DATA_FILE
from config import SOCKET_PATH


class Days(Enum):
    Mon = "monday"
    Tue = "tuesday"
    Wed = "wednesday"
    Thu = "thursday"
    Fri = "friday"
    Sat = "saturday"
    Sun = "sunday"


LOCK = Path("/tmp/notify-daemon.lock")
schedule_lock = Lock()


def set_notify(description):
    notification = Notify()
    notification.title = description
    notification.send()


def load_notifications():
    schedule.clear()

    data = json.loads(DATA_FILE.read_text())

    for record in data:
        for day in record["days"]:
            (
                getattr(schedule.every(), getattr(Days, day).value)
                .at(record["time"])
                .do(partial(set_notify, record.get("description")))
            )


def handle_command(cmd: str):
    if cmd == "reload":
        load_notifications()
        return b"ok"

    if cmd == "status":
        return b"alive"

    return b"unknown"


def daemon_process():
    if SOCKET_PATH.exists():
        SOCKET_PATH.unlink()

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(str(SOCKET_PATH))
    sock.listen()
    sock.setblocking(False)

    load_notifications()

    while True:
        try:
            conn, _ = sock.accept()
            cmd = conn.recv(1024).decode().strip()
            response = handle_command(cmd)
            conn.close()
        except BlockingIOError:
            pass

        schedule.run_pending()
        time.sleep(1)


daemon_process()
