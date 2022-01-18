from typing import TYPE_CHECKING
from datetime import datetime

from disnake import Embed


if TYPE_CHECKING:
    from disnake.embeds import MaybeEmpty
    from disnake.types.embed import EmbedType


class DefaultEmbed(Embed):
    def __init__(
        self,
        *,
        title: "MaybeEmpty[Any]" = Embed.Empty,
        type_: "EmbedType" = "rich",
        url: "MaybeEmpty[Any]" = Embed.Empty,
        description: "MaybeEmpty[Any]" = Embed.Empty,
        timestamp: datetime = None
    ) -> None:
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
    ) -> None:
        super().__init__(
            title="Info",
            description=description,
        )
