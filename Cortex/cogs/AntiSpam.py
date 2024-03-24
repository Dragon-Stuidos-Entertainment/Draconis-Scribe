import discord
from discord.ext import commands
import asyncio

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = {}
        self.muted_role_name = "Muted"  # Name of the muted role

    async def check_spam(self, message):
        author_id = message.author.id
        if author_id not in self.cooldown:
            self.cooldown[author_id] = 0
        
        if self.cooldown[author_id] > 0:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Please wait a moment before sending another message.")
            
            # Check if user has been warned multiple times
            if self.cooldown[author_id] > 2:
                await self.mute_user(message.author)
        else:
            self.cooldown[author_id] = 7  # Cooldown period in seconds
            await asyncio.sleep(3)
            self.cooldown[author_id] = 0

    async def mute_user(self, user):
        guild = user.guild
        muted_role = discord.utils.get(guild.roles, name=self.muted_role_name)
        if not muted_role:
            # Create the muted role if it doesn't exist
            muted_role = await guild.create_role(name=self.muted_role_name)

            # Apply the muted role to the user
            for channel in guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)
        
        # Assign the muted role to the user
        await user.add_roles(muted_role)
        await user.send("You have been muted for spamming.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        await self.check_spam(message)

def setup(bot):
    bot.add_cog(AntiSpam(bot))
