import discord
from discord.ext import commands
from discord.ext.commands import Context

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_polls = {}  # Store active polls in this dictionary

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Handle reactions for active polls
        if user == self.bot.user:
            return  # Ignore reactions by the bot

        if reaction.message.id in self.active_polls:
            poll = self.active_polls[reaction.message.id]
            if reaction.emoji == "✅":
                await reaction.message.remove_reaction("✅", user)
                if user.id not in poll["votes"]:
                    poll["votes"].append(user.id)
            elif reaction.emoji == "❌":
                await reaction.message.remove_reaction("❌", user)
                if user.id in poll["votes"]:
                    poll["votes"].remove(user.id)

    @commands.command(name="create_poll")
    async def create_poll(self, ctx: Context, question, *options):
        # Create a new poll
        if ctx.author.id in self.active_polls:
            await ctx.send("You already have an active poll. Finish or cancel it before creating a new one.")
            return

        if len(options) < 2:
            await ctx.send("You need to provide at least two options for the poll.")
            return

        poll = {"question": question, "options": list(options), "votes": []}
        self.active_polls[ctx.author.id] = poll

        # Send the poll as an embed
        poll_message = discord.Embed(title=f"Poll: {question}", description="React with ✅ or ❌ to vote.")
        poll_message.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

        for index, option in enumerate(options):
            poll_message.add_field(name=f"Option {index + 1}", value=option)

        poll_message.set_footer(text="Poll created by " + ctx.author.display_name)

        poll_message = await ctx.send(embed=poll_message)
        await poll_message.add_reaction("✅")
        await poll_message.add_reaction("❌")

    @commands.command(name="finish_poll")
    async def finish_poll(self, ctx: Context):
        # Finish the active poll and display results
        if ctx.author.id not in self.active_polls:
            await ctx.send("There is no active poll to finish.")
            return

        poll = self.active_polls.pop(ctx.author.id)
        yes_votes = 0
        no_votes = 0

        for user_id in poll["votes"]:
            member = ctx.guild.get_member(user_id)
            if member:
                if "✅" in [str(react) for react in member.activities]:
                    yes_votes += 1
                if "❌" in [str(react) for react in member.activities]:
                    no_votes += 1

        result_message = (
            f"Poll Results:\n"
            f"Question: {poll['question']}\n"
            f"Yes Votes: {yes_votes}\n"
            f"No Votes: {no_votes}"
        )

        await ctx.send(result_message)

    @commands.command(name="cancel_poll")
    async def cancel_poll(self, ctx: Context):
        # Cancel the active poll
        if ctx.author.id not in self.active_polls:
            await ctx.send("There is no active poll to cancel.")
            return

        self.active_polls.pop(ctx.author.id)
        await ctx.send("The active poll has been canceled.")

def setup(bot):
    bot.add_cog(Poll(bot))
