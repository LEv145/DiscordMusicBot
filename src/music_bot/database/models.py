"""Database models."""

from __future__ import annotations

from enum import Enum
from datetime import date, datetime

from dataclasses import dataclass


class Lang(Enum):
    rus = "rus"
    eng = "eng"


class SearchService(Enum):
    spotify = "spotify"


@dataclass
class Guild():
    id: int
    lang: Lang = Lang.eng


@dataclass
class Track():
    created_at: datetime
    url: str


@dataclass
class Member():
    id: int
    search_service: SearchService = SearchService.spotify
    premium_date_activate: date | None = None

