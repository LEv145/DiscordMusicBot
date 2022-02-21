from datetime import date
from dataclasses import dataclass


@dataclass
class Member():
    id: int
    premium_date_activate: date | None = None
