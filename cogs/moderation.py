import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member from the server."""
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member from the server."""
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Mute a member in the server."""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")  # Replace with your muted role name
        if muted_role is None:
            await ctx.send("Muted role not found. Please create one.")
            return

        # Add the "Muted" role to the member
        await member.add_roles(muted_role, reason=reason)

        # Prevent the member from talking in voice channels
        for channel in ctx.guild.voice_channels:
            await member.edit(mute=True, reason=f"Muted: {reason}")

        await ctx.send(f"{member.mention} has been muted. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a previously muted member."""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")  # Replace with your muted role name
        if muted_role is None:
            await ctx.send("Muted role not found. Please create one.")
            return

        # Remove the "Muted" role from the member
        await member.remove_roles(muted_role)

        # Allow the member to talk in voice channels
        for channel in ctx.guild.voice_channels:
            await member.edit(mute=False)

        await ctx.send(f"{member.mention} has been unmuted")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Clear a specified number of messages in the channel."""
        await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message

    @commands.command()
    async def ping(self, ctx):
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds
        await ctx.send(f"Pong! Bot latency is {latency}ms")

def setup(bot):
    bot.add_cog(Moderation(bot))
