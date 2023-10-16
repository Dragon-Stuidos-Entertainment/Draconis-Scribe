import discord
from discord.ext import commands

# Define a decorator for the cooldown
@commands.cooldown(1, 10)  # 1 use every 10 seconds

class AutoModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_history = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        user = message.author

        if user.id in self.message_history:
            time_difference = (message.created_at - self.message_history[user.id]).seconds

            if time_difference < 5:
                # User is sending messages too quickly
                if time_difference < 3:
                    # Check if the user has the "manage roles" permission
                    has_manage_roles_permission = any(role.permissions.manage_roles for role in user.roles)
                    
                    # Check if the user has the "Officer's" or "Enlisted NCO" roles
                    has_officer_role = any(role.name == "Officer's" for role in user.roles)
                    has_enlisted_nco_role = any(role.name == "Enlisted NCO" for role in user.roles)

                    # Apply the cooldown for specific roles
                    if not (has_manage_roles_permission or has_officer_role or has_enlisted_nco_role):
                        await self.trigger_moderation_actions(message)

                # Update the message history
                self.message_history[user.id] = message.created_at

    async def trigger_moderation_actions(self, message):
        user = message.author

        # User is sending messages very quickly, mute the user
        muted_role = discord.utils.get(message.guild.roles, name="Muted")  # Replace with your muted role name
        if muted_role:
            await message.author.add_roles(muted_role)
            await message.channel.send(f"{user.mention} has been muted for spamming.")
        else:
            await message.channel.send("Muted role not found. Please create one.")
        
        # Delete the spammy message
        await message.delete()

        # Warn the user
        warning_message = f"{user.mention}, please refrain from spamming."
        await message.channel.send(warning_message)

def setup(bot):
    bot.add_cog(AutoModeration(bot))
