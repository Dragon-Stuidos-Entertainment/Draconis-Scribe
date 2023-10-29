import discord
from discord.ext import commands

class Voting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.command()
async def startvote(self, ctx, question, *options):
    """Start a new vote."""
    if len(options) < 2 or len(options) > 10:
        await ctx.send("Please provide 2 to 10 options for the vote.")
        return

    # Create an embed for the vote
    embed = discord.Embed(title=question, color=discord.Color.blue())
    for i, option in enumerate(options):
        embed.add_field(name=f"Option {i+1}", value=option, inline=False)

    # Send the vote message
    vote_message = await ctx.send(embed=embed)

    # Add reactions for voting
    for i in range(len(options)):
        await vote_message.add_reaction(f"{i+1}\u20e3")  # Adding reaction emojis (1️⃣, 2️⃣, 3️⃣, ...)

@commands.command()
async def vote(self, ctx, option_number):
    """Vote for an option in the current vote."""
    try:
        option_number = int(option_number)
    except ValueError:
        await ctx.send("Please provide a valid option number to vote for.")
        return

    if option_number < 1:
        await ctx.send("Option numbers start from 1.")
        return

    # Find the message containing the vote
    async for message in ctx.channel.history(limit=10):
        if message.embeds and message.embeds[0].title:
            # Check if the message contains a vote with the same title
            if message.embeds[0].title == "Vote in Progress":
                vote_message = message
                break
    else:
        await ctx.send("No vote in progress. Start a vote with `!startvote`.")
        return

    # Check if the provided option number is within the range of options
    if option_number <= len(vote_message.embeds[0].fields):
        # Add the user's reaction to the vote message
        await vote_message.add_reaction(f"{option_number}\u20e3")
        await ctx.send(f"Your vote for option {option_number} has been recorded.")
    else:
        await ctx.send("Invalid option number. Please choose a valid option to vote for.")

def setup(bot):
    bot.add_cog(Voting(bot))
