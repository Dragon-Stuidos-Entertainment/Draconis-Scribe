import discord
from discord.ext import commands
from discord.ext.commands import Context
import asyncio

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_polls = {}  # Store active polls in this dictionary

    @commands.command(name="create_poll")
    async def create_poll(self, ctx: Context, duration: int, question, *options):
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

        poll_message += f"\nVote using the command: !vote <option_number> within {duration} seconds"
        poll_message = await ctx.send(poll_message)

        # Add reaction emojis to the poll message
        for i in range(1, len(options) + 1):
            emoji = f"{i}\N{COMBINING ENCLOSING KEYCAP}"
            await poll_message.add_reaction(emoji)

        # Set a timer to end the poll
        await asyncio.sleep(duration)
        await self.finish_poll(ctx.author.id, poll_message)

    async def finish_poll(self, author_id, poll_message):
        if author_id not in self.active_polls:
            return

        poll_data = self.active_polls.pop(author_id)
        poll = poll_data
        results = {option: 0 for option in poll["options"]}

        for vote in poll["votes"].values():
            results[poll["options"][vote - 1]] += 1

        result_message = "Poll Results:\n"
        for option, count in results.items():
            result_message += f"{option}: {count} votes\n"

        await poll_message.edit(content=result_message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return  # Ignore reactions by the bot

        for author_id, poll in self.active_polls.items():
            if reaction.message.content.startswith(poll["question"]):
                emoji = reaction.emoji
                emoji_str = emoji[0] if not emoji.isnumeric() else emoji
                if emoji_str in poll["options"]:
                    poll["votes"][user.id] = poll["options"].index(emoji_str) + 1
                    return

def setup(bot):
    bot.add_cog(Poll(bot))
