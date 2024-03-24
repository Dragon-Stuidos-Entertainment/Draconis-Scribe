import discord
from discord.ext import commands

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events = {}  # Dictionary to store event information

    @commands.command(name="createevent")
    async def create_event(self, ctx, *, event_name):
        # Create the event message
        event_message = await ctx.send(f"React with ✅ to sign up for the event: {event_name}")

        # Add the signup emoji to the message
        await event_message.add_reaction("✅")

        # Store event information
        self.events[event_name] = {"channel_id": ctx.channel.id, "message_id": event_message.id, "signup_emoji": "✅"}

        await ctx.send(f"Event created: {event_name}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Check if the reaction is for an event message
        event_info = self.events.get(payload.message_id)
        if event_info and str(payload.emoji) == event_info["signup_emoji"]:
            # Get the user and the channel
            user = await self.bot.fetch_user(payload.user_id)
            channel = self.bot.get_channel(payload.channel_id)

            # Send a confirmation message
            await channel.send(f"{user.mention} has signed up for the event!")

def setup(bot):
    bot.add_cog(Event(bot))
