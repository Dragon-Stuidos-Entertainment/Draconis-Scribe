import discord
from discord.ext import commands
import random

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="randomnumber")
    async def randomnumber(self, ctx, min_num: int, max_num: int):
        """Generate a random number within the specified range."""
        if min_num >= max_num:
            await ctx.send("Invalid range. Please specify a valid range.")
            return

        result = random.randint(min_num, max_num)
        await ctx.send(f"Random number between {min_num} and {max_num}: {result}")

    @commands.command(name="cointosses")
    async def cointosses(self, ctx, num_tosses: int = 1):
        """Simulate multiple coin tosses and report the results."""
        if num_tosses <= 0:
            await ctx.send("Invalid input. Please specify a valid number of coin tosses.")
            return

        results = [random.choice(["Heads", "Tails"]) for _ in range(num_tosses)]
        await ctx.send(f"Coin toss results: {', '.join(results)}")

    @commands.command(name="8ball")
    async def eightball(self, ctx, question):
        """Ask the magic 8-ball a question and get a random answer."""
        responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.",
                     "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
                     "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                     "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
                     "My sources say no.", "Outlook not so good.", "Very doubtful"]

        response = random.choice(responses)
        await ctx.send(f"Question: {question}\nMagic 8-Ball says: {response}")

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx):
        """Display information about the current server."""
        server = ctx.guild
        member_count = server.member_count
        online_members = sum(member.status == discord.Status.online for member in server.members)

        embed = discord.Embed(title=f"Server Information: {server.name}", color=discord.Color.blue())
        embed.add_field(name="Server Owner", value=server.owner, inline=True)
        embed.add_field(name="Server Region", value=server.region, inline=True)
        embed.add_field(name="Total Members", value=member_count, inline=True)
        embed.add_field(name="Online Members", value=online_members, inline=True)

        await ctx.send(embed=embed)

  @commands.command(name="whois")
async def whois(self, ctx, member: discord.Member):
    """Display information about a specific user."""
    user_status = str(member.status).capitalize()
    user_roles = ", ".join([role.mention for role in member.roles if role != ctx.guild.default_role])

    embed = discord.Embed(title=f"User Information: {member.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=member.avatar_url_as(static_format="png", size=1024))  # Specify format and size
    embed.add_field(name="User ID", value=member.id, inline=True)
    embed.add_field(name="User Status", value=user_status, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Registered", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Roles", value=user_roles, inline=False)

    await ctx.send(embed=embed)

@commands.command(name="avatar")
async def avatar(self, ctx, member: discord.Member = None):
    """Display a user's avatar."""
    if not member:
        member = ctx.author

    avatar_url = member.avatar_url_as(static_format="png", size=1024)  # You can specify format and size
    await ctx.send(avatar_url)



def setup(bot):
    bot.add_cog(Utility(bot))
