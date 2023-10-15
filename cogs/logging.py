import discord
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot, log_channel_id):
        self.bot = bot
        self.log_channel_id = log_channel_id

    async def log_to_channel(self, message):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(message)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        log_message = f"{user.name}#{user.discriminator} ({user.id}) was banned from {guild.name}."
        await self.log_to_channel(log_message)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log_message = f"{user.name}#{user.discriminator} ({user.id}) was unbanned from {guild.name}."
        await self.log_to_channel(log_message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_message = f"{member.name}#{member.discriminator} ({member.id}) joined the server."
        await self.log_to_channel(log_message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_message = f"{member.name}#{member.discriminator} ({member.id}) left the server."
        await self.log_to_channel(log_message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_message = f"Message by {message.author.name}#{message.author.discriminator} ({message.author.id}) deleted in {message.channel.name}:\n{message.content}"
        await self.log_to_channel(log_message)

    # You can add more event listeners for kicks, mutes, role changes, etc.

def setup(bot, log_channel_id):
    bot.add_cog(Logging(bot, log_channel_id))
