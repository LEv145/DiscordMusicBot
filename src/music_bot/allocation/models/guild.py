import enum
from dataclasses import dataclass


class Lang(enum.Enum):
    rus = "rus"
    eng = "eng"


@dataclass
class Guild():
    id: int
    lang: Lang = Lang.eng
