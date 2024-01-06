import discord
from discord.ext import commands

YOUR_AAR_CHANNEL_ID = 1188702656022184046  # Replace with the actual channel ID where AAR reports should be sent

class AAR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="submitaar")
    async def submit_aar(self, ctx):
        # Ask each portion of the AAR and delete the question once answered
        questions = [
            "After Action Report – **CLAN V. CLAN**",
            "DOA: **MONTH/DAY/YEAR**",
            "TOA: **TYPE OF ACTIVITY**",
            "POC: **PERSON OF CHARGE**",
            "OUT: **VICTORY/DEFEAT/TIE**",
            "\n__Personnel Attending__ – # of People",
            "\nOpposing Forces",
            "\nLeft Early (^)",
            "\nJoined Late (!)",
            "\n__Event Log__ [IF RAID WRITE A SUMMARY BELOW, IF NOT DELETE THIS BRACKETED MESSAGE]",
            "Game 1: The Pit CTF [5-2] Texas",
            "Game 2: Sanctuary Slayer [50-47] BLAM",
            "Game 3: Nexus KOTH [250-120] Texas",
            "\n__Event Comments__",
            "+ Good Communication",
            "+ Good Rotations",
            "– Complaining About Nades"
        ]

        responses = []

        for question in questions:
            message = await ctx.send(question)
            try:
                response = await self.bot.wait_for('message', timeout=300, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                responses.append(response.content)
                await message.delete()
            except discord.errors.NotFound:
                # Message may have been deleted by the user, ignore the error
                pass
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond. The AAR submission process has been canceled.")
                return

        # Combine the responses into a formatted AAR
        formatted_aar = "\n".join(responses)

        # Create an embed for the AAR
        embed = discord.Embed(title="After Action Report", color=discord.Color.blue())
        embed.description = formatted_aar

        # Send the embed to the specified channel
        aar_channel = self.bot.get_channel(YOUR_AAR_CHANNEL_ID)
        if aar_channel:
            await aar_channel.send(embed=embed)
            await ctx.send("Your After Action Report has been submitted successfully.")
        else:
            await ctx.send("AAR channel not found. Please contact the server administrator.")

def setup(bot):
    bot.add_cog(AAR(bot))
