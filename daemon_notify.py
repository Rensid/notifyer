import json
import time
from enum import Enum
from functools import partial
from pathlib import Path
from threading import Lock

import daemon
import schedule
from daemon import pidfile
from notifypy import Notify

from storage import DATA_FILE


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


def load_schedule():
    schedule.clear()

    data = json.loads(DATA_FILE.read_text())

    for record in data:
        for day in record["days"]:
            (
                getattr(schedule.every(), getattr(Days, day).value)
                .at(record["time"])
                .do(partial(set_notify, record.get("description")))
            )


def run():
    last_mtime = None

    while True:
        try:
            mtime = DATA_FILE.stat().st_mtime

            if last_mtime is None or mtime > last_mtime:
                load_schedule()
                last_mtime = mtime

            schedule.run_pending()
            time.sleep(1)

        except Exception as e:
            print(f"Scheduler error: {e}")
            time.sleep(5)


def daemon_process():
    print("Демон запущен")
    # with daemon.DaemonContext(pidfile=pidfile.TimeoutPIDLockFile(str(LOCK))):
    run()
