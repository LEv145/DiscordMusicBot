from __future__ import annotations

from typing import (
    Callable,
    Awaitable,
    Any,
    TypeVar,
)
from mypy_extensions import VarArg, KwArg

import lightbulb


PluginFunctionType = TypeVar(
    "PluginFunctionType",
    bound=Callable[[lightbulb.Context, VarArg(), KwArg()], Awaitable[None]],
)


def pass_options(function: PluginFunctionType) -> PluginFunctionType:
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
        await function(ctx, *ctx.raw_options.values(), *args, **kwargs)

    return decorated
