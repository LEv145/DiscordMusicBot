from dataclasses import dataclass
from datetime import datetime


@dataclass
class Track():
    created_at: datetime
    url: str
    name: str
