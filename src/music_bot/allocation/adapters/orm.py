"""ORM tables."""

from sqlalchemy import (
    Table,
    MetaData,
    Column,
)
from sqlalchemy.types import (
    Integer,
    String,
)
from sqlalchemy.orm import mapper

from ..models import (
    Member,
    Guild,
)


metadata = MetaData()

member_table = Table(
    "member", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
)


def start_mappers() -> None:
    mapper(Member, member_table)
