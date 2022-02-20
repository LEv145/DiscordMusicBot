import hikari_tools
import lightbulb


from bot import BaseBot


# noinspection PyAbstractClass
class BotContext(lightbulb.Context):
    bot: BaseBot
    guild: hikari_tools.Guild
    guild_id: hikari_tools.Snowflakeish

