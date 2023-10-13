import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount: int):
        # Your code to clear messages here

def setup(bot):
    bot.add_cog(Clear(bot))
