import discord
from discord.ext import commands

class ModerationLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = None  # Initialize to None

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
        await this.log_to_channel(log_message)

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

def setup(bot):
    cog = ModerationLogger(bot)
    bot.add_cog(cog)
