import typing as t
from datetime import datetime


def format_datetime(
    datetime_object: datetime,
    style: t.Literal['f', 'F', 'd', 'D', 't', 'T', 'R'] | None = None,
) -> str:
    """A helper function to format `datetime.datetime` for presentation within Discord.
    +-------------+----------------------------+-----------------+
    |    Style    |       Example Output       |   Description   |
    +=============+============================+=================+
    | t           | 22:57                      | Short Time      |
    +-------------+----------------------------+-----------------+
    | T           | 22:57:58                   | Long Time       |
    +-------------+----------------------------+-----------------+
    | d           | 17/05/2016                 | Short Date      |
    +-------------+----------------------------+-----------------+
    | D           | 17 May 2016                | Long Date       |
    +-------------+----------------------------+-----------------+
    | f (default) | 17 May 2016 22:57          | Short Date Time |
    +-------------+----------------------------+-----------------+
    | F           | Tuesday, 17 May 2016 22:57 | Long Date Time  |
    +-------------+----------------------------+-----------------+
    | R           | 5 years ago                | Relative Time   |
    +-------------+----------------------------+-----------------+
    """
    if style is None:
        return f"<t:{int(datetime_object.timestamp())}>"
    return f"t:{int(datetime_object.timestamp())}:{style}>"
