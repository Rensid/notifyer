from dataclasses import asdict, dataclass
from typing import List, Optional


@dataclass
class Notification:
    time: str
    days: list[str]
    description: str
    icon: str | None
    sound: str | None

    def to_dict(self):
        return asdict(self)
