import typing as t


_T = t.TypeVar("_T")


def shorten(
    string: str,
    width: int,
    placeholder: str = "[...]",
) -> str:
    if width < 0:
        raise ValueError("Invalid width value")

    return (
        string
        if len(string) <= width else
        string[:width - len(placeholder)] + placeholder
    )


def convert_optional_string(
    function: t.Callable[[_T], str],
    value: _T | None,
) -> str:
    if value is None:
        return ""
    return function(value)
