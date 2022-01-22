"""Database initialization"""
from typing import Final

from config import DATABASE_URL
from database import Database


database: Final = Database(url=DATABASE_URL)
