@bot.command()
async def ping(ctx):
    before = datetime.datetime.now()
    message = await ctx.send("Pinging...")
    after = datetime.datetime.now()
    latency = (after - before).total_seconds() * 1000
    await message.edit(content=f"Pong! Latency is {latency:.2f}ms")