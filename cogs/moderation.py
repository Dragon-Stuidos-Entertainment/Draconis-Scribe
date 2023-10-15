import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx, user: discord.Member, *, reason="No reason provided"):
        await user.ban(reason=reason)
        await ctx.send(f"{user.mention} has been banned. Reason: {reason}")

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        await ctx.send(f"{user.mention} has been kicked. Reason: {reason}")

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute_user(self, ctx, user: discord.Member, *, reason="No reason provided"):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")  # Replace with your muted role name
        if muted_role is None:
            await ctx.send("Muted role not found. Please create one.")
            return

        await user.add_roles(muted_role, reason=reason)
        await ctx.send(f"{user.mention} has been muted. Reason: {reason}")

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute_user(self, ctx, user: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")  # Replace with your muted role name
        if muted_role is None:
            await ctx.send("Muted role not found. Please create one.")
            return

        await user.remove_roles(muted_role)
        await ctx.send(f"{user.mention} has been unmuted")

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int = 5):
        await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message

    @commands.command(name="warn")
    @commands.has_permissions(kick_members=True)
    async def warn_user(self, ctx, user: discord.Member, *, reason="No reason provided"):
        # Implement your own warning system
        await ctx.send(f"{user.mention} has been warned. Reason: {reason}")

    @commands.command(name="tempban")
    @commands.has_permissions(ban_members=True)
    async def tempban_user(self, ctx, user: discord.Member, duration, *, reason="No reason provided"):
        # Implement temporary bans based on the 'duration' parameter
        await user.ban(reason=reason)
        await ctx.send(f"{user.mention} has been temporarily banned for {duration}. Reason: {reason}")

    @commands.command(name="tempmute")
    @commands.has_permissions(manage_roles=True)
    async def tempmute_user(self, ctx, user: discord.Member, duration, *, reason="No reason provided"):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")  # Replace with your muted role name
        if muted_role is None:
            await ctx.send("Muted role not found. Please create one.")
            return

        if muted_role not in user.roles:
            await user.add_roles(muted_role, reason=reason)
            await ctx.send(f"{user.mention} has been temporarily muted for {duration}. Reason: {reason}")
            # Implement a timer to remove the 'Muted' role after the specified duration
        else:
            await ctx.send(f"{user.mention} is already muted.")

    @commands.command(name="unwarn")
    @commands.has_permissions(kick_members=True)
    async def unwarn_user(self, ctx, user: discord.Member):
        # Implement your own warning system to remove warnings
        await ctx.send(f"{user.mention}'s warning has been removed.")

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
