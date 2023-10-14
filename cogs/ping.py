import discord
from discord.ext import commands
import datetime

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        before = datetime.datetime.now()
        message = await ctx.send("Pinging...")
        after = datetime.datetime.now()
        latency = (after - before).total_seconds() * 1000
        await message.edit(content=f"Pong! Latency is {latency:.2f}ms")

async def setup(bot):
    print(f"Setting up the Ping cog...")
    bot.add_cog(Ping(bot))
