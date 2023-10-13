import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount: int = 5):
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.channel.purge(limit=amount + 1)
        else:
            await ctx.send("You don't have permission to manage messages.")

def setup(bot):
    bot.add_cog(Clear(bot))
