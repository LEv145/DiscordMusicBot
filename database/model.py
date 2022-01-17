from __future__ import annotations

from typing import (
    Optional,
)
from enum import Enum
from datetime import date, datetime

from pydantic import BaseModel


class Guild(BaseModel):
    id: int
    lang: Lang


class Track(BaseModel):
    created_at: datetime
    url: str


class Member(BaseModel):
    id: int
    tracks_queue: list[Track]
    search_service: SearchService
    premium_date_activate: Optional[date]


class Lang(Enum):
    rus = "rus"
    eng = "eng"


class SearchService(Enum):
    spotify = "spotify"
