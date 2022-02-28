from datetime import datetime


class Track():
    def __init__(
        self,
        link: str,
        title: str | None,
        created_at: datetime | None = None,
    ):
        if created_at is not None:
            if created_at.tzinfo is None:
                raise ValueError("Datetime object without timezone")
            object_created_at = created_at
        else:
            object_created_at = datetime.now().astimezone()

        self.link: str = link
        self.title: str | None = title
        self.created_at: datetime = object_created_at

