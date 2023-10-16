import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_moderator_command(self, ctx, command_name, target):
        log_channel = self.bot.get_channel(1163150349511696484)  # Change the channel ID as needed
        if log_channel:
            log_message = f"Moderator {ctx.author} used the '{command_name}' command on {target}."
            await log_channel.send(log_message)

    def delete_command_message(self, ctx):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx, user: discord.Member, *, reason="No reason provided"):
        await user.ban(reason=reason)
        await ctx.send(f"{user.mention} has been banned. Reason: {reason}")

        # Log the command and delete it
        await self.log_moderator_command(ctx, "ban", user)
        self.delete_command_message(ctx)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        await ctx.send(f"{user.mention} has been kicked. Reason: {reason}")

        # Log the command and delete it
        await self.log_moderator_command(ctx, "kick", user)
        self.delete_command_message(ctx)

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute_user(self, ctx, user: discord.Member, *, reason="No reason provided"):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")  # Replace with your muted role name
        if muted_role is None:
            await ctx.send("Muted role not found. Please create one.")
            return

        await user.add_roles(muted_role, reason=reason)
        await ctx.send(f"{user.mention} has been muted. Reason: {reason}")

        # Log the command and delete it
        await self.log_moderator_command(ctx, "mute", user)
        self.delete_command_message(ctx)

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute_user(self, ctx, user: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")  # Replace with your muted role name
        if muted_role is None:
            await ctx.send("Muted role not found. Please create one.")
            return

        await user.remove_roles(muted_role)
        await ctx.send(f"{user.mention} has been unmuted")

        # Log the command and delete it
        await self.log_moderator_command(ctx, "unmute", user)
        self.delete_command_message(ctx)

    @commands.command(name="warn")
    @commands.has_permissions(kick_members=True)
    async def warn_user(self, ctx, user: discord.Member, *, reason="No reason provided"):
        # Implement your own warning system
        await ctx.send(f"{user.mention} has been warned. Reason: {reason}")

        # Log the command and delete it
        await self.log_moderator_command(ctx, "warn", user)
        self.delete_command_message(ctx)

    @commands.command(name="tempban")
    @commands.has_permissions(ban_members=True)
    async def tempban_user(self, ctx, user: discord.Member, duration, *, reason="No reason provided"):
        # Implement temporary bans based on the 'duration' parameter
        await user.ban(reason=reason)
        await ctx.send(f"{user.mention} has been temporarily banned for {duration}. Reason: {reason}")

        # Log the command and delete it
        await self.log_moderator_command(ctx, "tempban", user)
        self.delete_command_message(ctx)

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

        # Log the command and delete it
        await self.log_moderator_command(ctx, "tempmute", user)
        self.delete_command_message(ctx)

    @commands.command(name="unwarn")
    @commands.has_permissions(kick_members=True)
    async def unwarn_user(self, ctx, user: discord.Member):
        # Implement your own warning system to remove warnings
        await ctx.send(f"{user.mention}'s warning has been removed.")

        # Log the command and delete it
        await self.log_moderator_command(ctx, "unwarn", user)
        self.delete_command_message(ctx)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Clear a specified number of messages in the channel."""
        await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message

        # Log the command and delete it
        await self.log_moderator_command(ctx, "clear", ctx.channel)
        self.delete_command_message(ctx)

    @commands.command()
    async def ping(self, ctx):
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds
        await ctx.send(f"Pong! Bot latency is {latency}ms")

def setup(bot):
    bot.add_cog(Moderation(bot))
