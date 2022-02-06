import unittest
from unittest.mock import Mock

from models.repository import DictVoiceRepository


class TestDictVoiceRepository(unittest.IsolatedAsyncioTestCase):
    async def test(self) -> None:
        repository = DictVoiceRepository()

        await repository.add(1, Mock(id=1))
        await repository.add(1, Mock(id=2))
        self.assertEqual((await repository.get(1)).id, 1)

        await repository.remove(1)
        self.assertIsNone(await repository.get(1))


