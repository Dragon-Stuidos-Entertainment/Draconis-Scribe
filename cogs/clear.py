@bot.command()
async def clear(ctx, amount=5):
    if ctx.message.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
    else:
        await ctx.send("You don't have permission to manage messages.")