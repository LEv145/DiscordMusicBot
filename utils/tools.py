# TODO: https://breadcrumbscollector.tech/where-to-put-all-your-utils-in-python-projects/
from typing import Any, Optional
from datetime import timedelta
from string import Template


class DeltatimeTemplate(Template):
    delimiter = "%"


def strdelta(delta: timedelta, format_string: str) -> str:
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
