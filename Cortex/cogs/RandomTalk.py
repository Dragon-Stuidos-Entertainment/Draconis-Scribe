import discord
import random
import asyncio
from discord.ext import commands

class RandomTalk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None  # Initialize the channel variable
        self.messages = [
            "Hello, everyone! This is your friendly AI ship speaking.",
            "Just checking in to let you know everything is going well.",
            "Did you know that I can help you with any questions you have?",
            "If you have any concerns, please don't hesitate to let me know.",
            "I'm always here to assist you with any problems you may have."
        ]  # List of possible messages

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(channel_id)  # Get the channel where you want the bot to talk
        self.bot.loop.create_task(self.send_periodic_message())  # Start the task for sending periodic messages

    async def send_periodic_message(self):
        """Send a random message to the designated channel every 3 hours"""
        while True:
            if self.channel:
                message = random.choice(self.messages)  # Select a random message from the list
                await self.channel.send(message)
            await asyncio.sleep(10800)  # Sleep for 3 hours (3 hours * 60 minutes * 60 seconds = 10800 seconds)

    @commands.command()
    async def add_message(self, ctx, *, message):
        """Add a new message to the list of possible messages"""
        self.messages.append(message)
        await ctx.send("Message added!")

    @commands.command()
    async def remove_message(self, ctx, index):
        """Remove a message from the list of possible messages"""
        try:
            self.messages.pop(index)
            await ctx.send("Message removed!")
        except IndexError:
            await ctx.send("Invalid index.")