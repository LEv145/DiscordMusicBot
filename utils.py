from typing import TYPE_CHECKING, Any, Optional
from datetime import datetime, timedelta
from string import Template

from disnake import Embed


if TYPE_CHECKING:
    from disnake.embeds import MaybeEmpty
    from disnake.types.embed import EmbedType


class DeltatimeTemplate(Template):
    delimiter = "%"


def strdelta(delta: timedelta, format_string: str):
    data = {}
    data["H"], remains = divmod(delta.seconds, 3600)
    data["M"], data["S"] = divmod(remains, 60)
    data["D"] = delta.days
    data["MS"] = delta.microseconds
    template = DeltatimeTemplate(format_string)
    return template.substitute(**data)


def bool_to_emoji(boolean: bool) -> str:
    if boolean:
        return "\N{LARGE GREEN CIRCLE}"
    return "\N{LARGE RED CIRCLE}"


def shorten(string: str, width: int, placeholder: str = "[...]") -> str:
    if len(string) <= width:
        return string

    width -= len(placeholder)

    if width < 0:
        raise ValueError

    return string[:width] + placeholder


def format_optional_string(template: str, value: Optional[Any]) -> str:
    if value is None:
        return ""
    return template.format(value)


class DefaultEmbed(Embed):
    def __init__(
        self,
        *,
        title: "MaybeEmpty[Any]" = Embed.Empty,
        type_: "EmbedType" = "rich",
        url: "MaybeEmpty[Any]" = Embed.Empty,
        description: "MaybeEmpty[Any]" = Embed.Empty,
        timestamp: datetime = None
    ):
        super().__init__(
            color=0xDD2828,
            title=title,
            type=type_,
            url=url,
            description=description,
            timestamp=timestamp,
        )


class InfoDefaultEmbed(DefaultEmbed):
    def __init__(
        self,
        description: str = None,
    ):
        super().__init__(
            title="Info",
            description=description,
        )
