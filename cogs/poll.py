import discord
from discord.ext import commands
from discord.ext.commands import Context
import asyncio  # Add this import for handling duration

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_polls = {}  # Store active polls in this dictionary

    @commands.command(name="create_poll")
    async def create_poll(self, ctx: Context, question, duration: int, *options):
        # Create a new poll
        if ctx.author.id in self.active_polls:
            await ctx.send("You already have an active poll. Finish or cancel it before creating a new one.")
            return

        if len(options) < 2:
            await ctx.send("You need to provide at least two options for the poll.")
            return

        poll = {"question": question, "options": list(options), "votes": {}}
        self.active_polls[ctx.author.id] = poll

        # Send the poll to the channel
        poll_message = f"**{question}**\n"
        for index, option in enumerate(options):
            poll_message += f"{index + 1}. {option}\n"

        poll_message += "\nVote using the command: !vote <option_number>"
        await ctx.send(poll_message)

        # Set up a timer to automatically finish the poll after the specified duration
        await asyncio.sleep(duration)
        await self.finish_poll(ctx)

    # ... (other commands remain the same)

def setup(bot):
    bot.add_cog(Poll(bot))
