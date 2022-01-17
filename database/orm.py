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

import model


metadata = MetaData()

member = Table(
    "member", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
)


def start_mappers():
    mapper(
        model.Member,
        member,
    )
