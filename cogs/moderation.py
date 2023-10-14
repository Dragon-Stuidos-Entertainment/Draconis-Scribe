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
        if muted_role
