from typing import (
    Any,
)
from datetime import datetime

from hikari import (
    Embed,
    Color,
)


class DefaultEmbed(Embed):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            color=Color(0x18c79d),
            timestamp=datetime.now().astimezone(),
            **kwargs,
        )
        self.set_footer(
            text=(
                "\N{Copyright Sign} All rights belong to the pony. "
                "The whole world belongs to ponies"
            ),
        )
