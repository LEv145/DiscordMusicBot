import abc

from allocation.models import Guild


class ABCGuildRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, guild: Guild) -> None:
        """Add guild to DB."""

    @abc.abstractmethod
    async def get(self, guild_id: int) -> Guild | None:
        """Get guild from DB."""
