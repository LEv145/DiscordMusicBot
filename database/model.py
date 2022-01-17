from typing import (
    Optional,
    List,
)
from enum import Enum
from dataclasses import dataclass
from datetime import date, datetime


class Lang(Enum):
    rus = "rus"
    eng = "eng"


class SearchService(Enum):
    spotify = "spotify"


@dataclass
class Guild():
    id: int
    lang: Lang


class Track():
    created_at: datetime
    url: str


@dataclass
class Member():
    id: int
    tracks_queue: List[Track]
    search_service: SearchService
    premium_date_activate: Optional[date]
