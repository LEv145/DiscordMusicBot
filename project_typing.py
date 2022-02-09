import hikari
import lightbulb


from models.bot import BaseBot


# noinspection PyAbstractClass
class BotContext(lightbulb.Context):
    bot: BaseBot
    guild: hikari.Guild
    guild_id: hikari.Snowflakeish

