import lightbulb


plugin = lightbulb.Plugin("Music")


@plugin.command()
@lightbulb.command(name="ping", description="Ping!")
@lightbulb.implements(lightbulb.PrefixCommand)
async def foo(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
