from __future__ import annotations

from typing import (
    Callable,
    Awaitable,
    Any,
)
from mypy_extensions import Arg, VarArg, KwArg

import lightbulb


def pass_options(
    func: Callable[[Arg(lightbulb.Context), VarArg(), KwArg()], Awaitable[None]],
) -> Callable[[lightbulb.Context], Awaitable[None]]:
    """
    First order decorator that causes the decorated command callback function
    to have all options provided by the context passed as **keyword** arguments
    on invocation. This allows you to access the options directly instead of through the
    context object.

    This decorator **must** be below all other command decorators.

    Example:

        .. code-block:: python

            @lightbulb.option("text", "Text to repeat")
            @pass_options
            async def echo(ctx, text):
                await ctx.respond(text)
    """

    async def decorated(ctx: lightbulb.Context, *args: Any, **kwargs: Any) -> None:
        return await func(ctx, *ctx.raw_options.values(), *args, **kwargs)

    return decorated
