import discord
from discord.ext import commands

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, target, *, message):
        """Send an announcement to a specific channel or role."""

        # Check if the command was used in a guild (server)
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server (guild).")
            return

        # Try to resolve the mentioned target (channel or role)
        resolved_target = None

        # Resolve a channel mention
        if ctx.message.channel_mentions:
            resolved_target = ctx.message.channel_mentions[0]

        # Resolve a role mention
        if not resolved_target and ctx.message.role_mentions:
            resolved_target = ctx.message.role_mentions[0]

        if not resolved_target:
            await ctx.send("Invalid target. Please mention a channel or role to send the announcement.")
            return

        # Send the announcement to the resolved target
        await resolved_target.send(f"Announcement from {ctx.author.mention}:\n{message}")

def setup(bot):
    bot.add_cog(Announcements(bot))
