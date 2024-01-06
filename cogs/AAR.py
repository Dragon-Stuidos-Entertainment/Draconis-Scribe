import discord
from discord.ext import commands

class AAR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.aar_reports = {}  # Dictionary to store AAR reports

    @commands.command(name="submitaar")
    async def submit_aar(self, ctx):
        def check_author(message):
            return message.author == ctx.author and message.channel == ctx.channel

        # Ask for DOA
        await ctx.send("Enter the Date of Action (DOA) in the format `MONTH/DAY/YEAR`:")
        doa_message = await self.bot.wait_for('message', check=check_author)
        doa = doa_message.content
        await doa_message.delete()

        # Ask for TOA
        await ctx.send("Enter the Type of Activity (TOA):")
        toa_message = await self.bot.wait_for('message', check=check_author)
        toa = toa_message.content
        await toa_message.delete()

        # Ask for POC
        await ctx.send("Enter the Person of Charge (POC):")
        poc_message = await self.bot.wait_for('message', check=check_author)
        poc = poc_message.content
        await poc_message.delete()

        # Ask for OUT
        await ctx.send("Enter the Outcome (OUT - Victory/Defeat/Tie):")
        out_message = await self.bot.wait_for('message', check=check_author)
        out = out_message.content
        await out_message.delete()

        # Ask for Personnel Attending
        await ctx.send("Enter the personnel attending in the format `CLAN'S EMOJI @Name`, one per line. Type `done` when finished:")
        personnel_lines = []
        while True:
            personnel_message = await self.bot.wait_for('message', check=check_author)
            if personnel_message.content.lower() == 'done':
                break
            personnel_lines.append(personnel_message.content)
            await personnel_message.delete()

        # Ask for Opposing Forces
        await ctx.send("Enter the opposing forces in the format `CLAN'S EMOJI Example Name`, one per line. Type `done` when finished:")
        forces_lines = []
        while True:
            forces_message = await self.bot.wait_for('message', check=check_author)
            if forces_message.content.lower() == 'done':
                break
            forces_lines.append(forces_message.content)
            await forces_message.delete()

        # Create an embed for the AAR report
        embed = discord.Embed(title="After Action Report", color=discord.Color.dark_green())
        embed.add_field(name="DOA", value=doa, inline=True)
        embed.add_field(name="TOA", value=toa, inline=True)
        embed.add_field(name="POC", value=poc, inline=True)
        embed.add_field(name="OUT", value=out, inline=True)

        # Add personnel attending to the embed
        embed.add_field(name="Personnel Attending", value="\n".join(personnel_lines), inline=False)

        # Add opposing forces to the embed
        embed.add_field(name="Opposing Forces", value="\n".join(forces_lines), inline=False)

        # Send the AAR report as an embed
        aar_channel = self.bot.get_channel(YOUR_AAR_CHANNEL_ID)  # Replace with the actual channel ID
        if aar_channel:
            message = await aar_channel.send(embed=embed)
            self.aar_reports[ctx.author.id] = {"message_id": message.id}

            # Add reactions for additional comments
            await message.add_reaction("👍")  # Positive
            await message.add_reaction("👎")  # Negative
            await message.add_reaction("❓")  # Questions

            await ctx.send("AAR report submitted successfully.")
        else:
            await ctx.send("AAR channel not found. Please contact the server administrator.")

def setup(bot):
    bot.add_cog(AAR(bot))
