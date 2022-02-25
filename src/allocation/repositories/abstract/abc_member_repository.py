import abc

from allocation.models import Member


class ABCMemberRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, member: Member) -> None:
        """Add member to DB."""

    @abc.abstractmethod
    async def get(self, member_id: int) -> Member | None:
        """Get member from DB."""
