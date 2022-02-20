import lightbulb


@lightbulb.Check
async def check_author_in_voice_channel(ctx: lightbulb.Context) -> bool:
    states = ctx.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_states = states.iterator().filter(lambda i: i.user_id == ctx.author.id)

    try:
        await voice_states.__anext__()
    except StopAsyncIteration:
        return False
    return True
