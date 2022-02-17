import typing
import copy
import inspect

import lightbulb


class BasePluginManager():
    def __init__(
        self,
        name: str, description: str | None = None,
        **kwargs: typing.Any,
    ):
        self._plugin = lightbulb.Plugin(
            name=name,
            description=description,
            **kwargs,
        )

    def load_commands(self, cls: typing.Any) -> None:
        command: lightbulb.CommandLike
        for name, command in inspect.getmembers(
            object=cls,
            predicate=lambda value: isinstance(value, lightbulb.CommandLike),
        ):
            self._plugin.command(command)

    def get_plugin(self) -> lightbulb.Plugin:
        return copy.copy(self._plugin)
