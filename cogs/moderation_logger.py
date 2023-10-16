import discord
from discord.ext import commands

class ModerationLogger(commands.Cog):
    def __init__(self, bot, log_channel_id):
        self.bot = bot
        self.log_channel_id = log_channel_id

    def get_log_channel(self):
        # Return the log channel from the provided ID
        return self.bot.get_channel(self.log_channel_id)

    async def log_to_channel(self, message):
        log_channel = self.get_log_channel()
        if log_channel:
            await log_channel.send(message)

    # ... (previously defined methods)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        log_message = self.format_log_message(guild.me, user, "banned", None)
        await self.log_to_channel(log_message)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log_message = self.format_log_message(guild.me, user, "unbanned", None)
        await self.log_to_channel(log_message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_message = f"{message.author} ({message.author.id}) deleted a message in {message.channel}:"
        log_message += f"\nContent: {message.content}\n"
        await self.log_to_channel(log_message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_message = f"{member} ({member.id}) joined the server."
        await self.log_to_channel(log_message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_message = f"{member} ({member.id}) left the server."
        await self.log_to_channel(log_message)

# Rest of your code
