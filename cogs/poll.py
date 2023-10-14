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

        # Create an embedded poll message
        poll_embed = discord.Embed(title=f"**{question}**", description="Vote by reacting with ✅ or ❌")

        for index, option in enumerate(options):
            poll_embed.add_field(name=f"Option {index + 1}", value=option, inline=False)

        poll_message = await ctx.send(embed=poll_embed)
        await poll_message.add_reaction("✅")  # Add ✅ reaction
        await poll_message.add_reaction("❌")  # Add ❌ reaction

        # Delete the command message
        await ctx.message.delete()

    @commands.command(name="finish_poll")
    async def finish_poll(self, ctx: commands.Context):
        # Finish the active poll and display results
        if ctx.author.id not in self.active_polls:
            await ctx.send("There is no active poll to finish.")
            return

        poll = self.active_polls.pop(ctx.author.id)
        results = {option: 0 for option in poll["options"]}

        # Fetch the poll message for reactions
        async for message in ctx.channel.history(limit=1):
            if message.id == poll_message.id:
                poll_message = message
                break

        for reaction in poll_message.reactions:
            if reaction.emoji == "✅":
                results[poll["options"][0]] = reaction.count
            elif reaction.emoji == "❌":
                results[poll["options"][1]] = reaction.count

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
