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

import models


metadata = MetaData()

member_table = Table(
    "member", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
)


def start_mappers() -> None:  # TODO: Check mappers is running
    mapper(
        models.Member,
        member_table,
    )
