import discord
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_polls = {}  # Store active polls in this dictionary

    @commands.command(name="create_poll")
    async def create_poll(self, ctx: commands.Context, question, *options):
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

    @commands.command(name="vote")
    async def vote(self, ctx: commands.Context, option_number: int):
        # Allow users to vote in the active poll
        if ctx.author.id not in self.active_polls:
            await ctx.send("There is no active poll to vote in.")
            return

        poll = self.active_polls[ctx.author.id]
        if option_number < 1 or option_number > len(poll["options"]):
            await ctx.send("Invalid option number. Please vote for a valid option.")
            return

        user_id = ctx.author.id
        poll["votes"][user_id] = option_number
        await ctx.send(f"Your vote for option {option_number} has been recorded.")

    @commands.command(name="finish_poll")
    async def finish_poll(self, ctx: commands.Context):
        # Finish the active poll and display results
        if ctx author.id not in self.active_polls:
            await ctx.send("There is no active poll to finish.")
            return

        poll = self.active_polls.pop(ctx.author.id)
        results = {option: 0 for option in poll["options"]}

        for vote in poll["votes"].values():
            results[poll["options"][vote - 1]] += 1

        result_message = "Poll Results:\n"
        for option, count in results.items():
            result_message += f"{option}: {count} votes\n"

        await ctx.send(result_message)

    @commands.command(name="cancel_poll")
    async def cancel_poll(self, ctx: commands.Context):
        # Cancel the active poll
        if ctx.author.id not in self.active_polls:
            await ctx.send("There is no active poll to cancel.")
            return

        self.active_polls.pop(ctx.author.id)
        await ctx.send("The active poll has been canceled.")

def setup(bot):
    bot.add_cog(Poll(bot))
