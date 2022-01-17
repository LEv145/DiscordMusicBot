# from datetime import datetime, date, timedelta
# from typing import Any
#
# from tortoise.models import Model
# from tortoise import fields
#
# from database.enums import Lang
# from modules.music_source import SearchService
#
#
# class LastSavedTrack(Model):
#     id: int = fields.BigIntField(pk=True)
#
#     data: dict[str, Any] = fields.JSONField()
#     member: fields.OneToOneRelation["Member"] = fields.OneToOneField(
#         model_name="models.Member", related_name="last_saved_track"
#     )  # type: ignore
#     start_time: timedelta = fields.TimeDeltaField()
#
#     created_at: datetime = fields.DatetimeField(auto_now_add=True)
#
#     class Meta:
#         table = "last_saved_track"
#
#
# class TracksHistory(Model):
#     id: int = fields.BigIntField(pk=True)
#
#     data: dict[str, Any] = fields.JSONField()
#     member: fields.ForeignKeyRelation["Member"] = fields.ForeignKeyField(
#         model_name="models.Member", related_name="tracks_history"
#     )  # type: ignore
#
#     created_at: datetime = fields.DatetimeField(auto_now_add=True)
#
#     class Meta:
#         table = "tracks_history"
#
#
# class TracksQueue(Model):
#     id: int = fields.BigIntField(pk=True)
#
#     data: dict[str, Any] = fields.JSONField()
#     member: fields.ForeignKeyRelation["Member"] = fields.ForeignKeyField(
#         model_name="models.Member", related_name="tracks_queue"
#     )  # type: ignore
#
#     created_at: datetime = fields.DatetimeField(auto_now_add=True)
#
#     class Meta:
#         table = "tracks_queue"
#
#
# class Member(Model):
#     id: int = fields.BigIntField(pk=True, null=False)
#
#     tracks_queue: fields.ReverseRelation[TracksQueue]
#     tracks_history: fields.ReverseRelation[TracksHistory]
#     last_saved_track: fields.OneToOneRelation[LastSavedTrack]
#
#     search_service: SearchService = fields.CharEnumField(
#         SearchService, default=SearchService.youtube
#     )
#
#
# class Guild(Model):
#     id: int = fields.BigIntField(pk=True, null=False)
#
#     lang: Lang = fields.CharEnumField(Lang, default=Lang.eng)
#     premium: bool = fields.BooleanField(default=False)  # type: ignore
#     premium_date_activate: date = fields.DateField(null=True)
from .abc_repository import (
    ABCGuildRepository,
    ABCMemberRepository,
)

from .model import (
    Member,
    Guild,
    Lang,
)


class GuildRepository(ABCGuildRepository):
    async def add(self, guild: Guild) -> None:
        """Add guild to DB."""

    async def get(self, guild_id: int):
        """Get guild from DB."""

    async def set_lang(self, lang: Lang) -> None:
        """Set guild lang."""


class MemberRepository(ABCMemberRepository):
    async def add(self, member: Member) -> None:
        """Add member to DB."""

    async def get(self, member_id: int) -> Member:
        """Get member from DB."""
