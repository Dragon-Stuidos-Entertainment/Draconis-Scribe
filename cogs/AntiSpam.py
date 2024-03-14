import discord
from discord.ext import commands
import asyncio

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = {}

    async def check_spam(self, message):
        author_id = message.author.id
        if author_id not in self.cooldown:
            self.cooldown[author_id] = 0
        
        if self.cooldown[author_id] > 0:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Please wait a moment before sending another message.")
        else:
            self.cooldown[author_id] = 3  # Cooldown period in seconds
            await asyncio.sleep(3)
            self.cooldown[author_id] = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        await self.check_spam(message)

def setup(bot):
    bot.add_cog(AntiSpam(bot))
