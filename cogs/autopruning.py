import discord
from discord.ext import commands

class AutoPruning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.command()
@commands.has_permissions(administrator=True)
async def prune_inactive(self, ctx, days: int = 30):
    """
    Remove inactive members who haven't been online in X days.
    Usage: !prune_inactive [days]
    """
    # Define a variable to store the number of pruned members
    pruned_count = 0

    # Iterate through all members in the server
    for member in ctx.guild.members:
        # Check if the member is a bot or if they have a role that exempts them from pruning
        if not member.bot and not any(role.name.lower() in ["exempt_role1", "exempt_role2"] for role in member.roles):
            # Check the member's last online status
            last_online = member.status if member.status != discord.Status.offline else "offline"
            if last_online == "offline":
                last_online = member.status

            # Calculate the number of days since their last online activity
            delta = (ctx.message.created_at - member.joined_at).days

            # Check if the member hasn't been online for the specified number of days
            if delta >= days:
                try:
                    await member.kick(reason=f"Inactive for {days} days")
                    pruned_count += 1
                except Exception as e:
                    print(f"Failed to kick {member}: {e}")

    await ctx.send(f"{pruned_count} members have been pruned.")

def setup(bot):
    bot.add_cog(AutoPruning(bot))
