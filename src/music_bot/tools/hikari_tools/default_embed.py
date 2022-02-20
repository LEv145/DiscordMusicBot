import typing
from datetime import datetime

import hikari


class DefaultEmbed(hikari.Embed):
    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(
            color=hikari.Color(0x18c79d),
            timestamp=datetime.now().astimezone(),
            **kwargs,
        )
        self.set_footer(
            text=(
                "\N{Copyright Sign} All rights belong to the pony. "
                "The whole world belongs to ponies"
            ),
        )
