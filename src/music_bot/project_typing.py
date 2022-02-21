import hikari
import lightbulb


from tools.lightbulb.bot import BaseBot


# noinspection PyAbstractClass
class BotContext(lightbulb.Context):
    bot: BaseBot
    guild: hikari.Guild
    guild_id: hikari.Snowflakeish

