import disnake
from disnake.ext import commands, tasks
from loguru import logger


class Bot(commands.InteractionBot):
    """My BOt"""

    def __init__(self) -> None:
        super().__init__(
            intents=disnake.Intents.all()
        )
        self.update_description.start()

    async def on_ready(self) -> None:
        logger.info(f"We have logged in as {self.user}")

    @tasks.loop(seconds=10)
    async def update_description(self) -> None:
        if self.is_ready():
            activity = disnake.Activity(
                name=f"{len(self.guilds)} servers", type=disnake.ActivityType.listening
            )
            status = disnake.Status.online
            await self.change_presence(activity=activity, status=status)
