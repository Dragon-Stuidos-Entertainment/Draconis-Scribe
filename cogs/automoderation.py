import discord
from discord.ext import commands

# Define a decorator for the cooldown
@commands.cooldown(1, 10)  # 1 use every 10 seconds

class AutoModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_history = []
        self.bad_words = set()  # Store bad words in a set

        # Read bad words from the text file
        with open("bad_words.txt", "r") as file:
            self.bad_words.update(word.strip() for word in file.readlines())

    # Function to check for bad words
    async def check_bad_words(self, message):
        # Convert the message content to lowercase for case-insensitive matching
        content = message.content.lower()

        # Check if the message contains any bad words
        for word in self.bad_words:
            if word in content:
                # Delete the message with a warning
                await message.delete()

                # Warn the user
                warning_message = f"{message.author.mention}, please refrain from using bad language."
                await message.channel.send(warning_message)

                # You can also send a notification to your moderation log channel
                await self.send_spam_notification(message)

                return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        user = message.author

        # Check for bad words
        await self.check_bad_words(message)

        if user.id in self.message_history:
            time_difference = (message.created_at - self.message_history[user.id]).seconds

            if time_difference < 5:
                # User is sending messages too quickly
                if time_difference < 3:
                    has_manage_roles_permission = any(role.permissions.manage_roles for role in user.roles)
                    has_officer_role = any(role.name == "Officer's Core" for role in user.roles)
                    has_enlisted_nco_role = any(role.name == "Enlisted NCO" for role in user.roles)

                    if not (has_manage_roles_permission or has_officer_role or has_enlisted_nco_role):
                        await self.trigger_moderation_actions(message)

                self.message_history[user.id] = message.created_at

    async def send_spam_notification(self, message):
        log_channel = self.bot.get_channel(1163150349511696484)  # Change the channel ID as needed
        if log_channel:
            notification_message = f"Spam Message Notification: {message.author} ({message.author.id}) sent a spam message in {message.channel}:\nContent: {message.content}"
            await log_channel.send(notification_message)

    async def trigger_moderation_actions(self, message):
        user = message.author

        # User is sending messages very quickly, mute the user
        muted_role = discord.utils.get(message.guild.roles, name="Muted")  # Replace with your muted role name
        if muted_role:
            await message.author.add_roles(muted_role)
            await message.channel.send(f"{user.mention} has been muted for spamming.")
            await self.send_spam_notification(message)  # Send the spam notification
        else:
            await message.channel.send("Muted role not found. Please create one.")

        # Delete the spammy message
        await message.delete()

        # Warn the user
        warning_message = f"{user.mention}, please refrain from spamming."
        await message.channel.send(warning_message)

def setup(bot):
    bot.add_cog(AutoModeration(bot))
