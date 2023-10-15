import discord
from discord.ext import commands

class ModerationLogger(commands.Cog):
    def __init__(self, bot, log_channel_id):
        self.bot = bot
        self.log_channel_id = log_channel_id

    def format_log_message(self, ctx, target, action, reason):
        log_message = f"{ctx.author} ({ctx.author.id}) {action} {target} ({target.id})"
        if reason:
            log_message += f" for the reason: {reason}"
        return log_message

    async def log_to_channel(self, log_message):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(log_message)

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

    # You can add more event listeners for kicks, mutes, etc.

def setup(bot, log_channel_id):
    bot.add_cog(ModerationLogger(bot, log_channel_id))  # Fix the closing parenthesis here
