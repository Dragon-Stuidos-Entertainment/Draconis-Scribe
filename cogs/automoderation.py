import discord
from discord.ext import commands

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
            elif time_difference < 3:
                # User is sending messages very quickly, consider additional actions
                # You've already muted the user in this case, but you can add more actions if needed.

            self.message_history[user.id] = message.created_at

def setup(bot):
    bot.add_cog(AutoModeration(bot))
