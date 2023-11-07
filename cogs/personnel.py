import discord
from discord.ext import commands
import json

# Read the JSON data
with open('personnel_records.json', 'r') as file:
    personnel_data = json.load(file)

class Personnel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def searchrecord(self, ctx, name):
        # Check if the user has the "TopSecret" role
        if "TopSecret" in [role.name for role in ctx.author.roles]:
            matching_records = []

            # Search for records with a matching name
            for record in personnel_data["personnel_records"]:
                if name.lower() in record["name"].lower():
                    matching_records.append(record)

            if matching_records:
                # Send information for all matching records
                for record in matching_records:
                    embed = discord.Embed(
                        title=record['name'],
                        description=f"Position: {record['position']}\nDepartment: {record['department']}\nEmail: {record['email']}\nRank: {record['rank']}\nGamertag: {record['gamertag']}\nMID: {record['mid']}\nYears of Service: {record['YOS']}",
                        color=0x00ff00
                    )
                    await ctx.send(embed=embed)
            else:
                await ctx.send("No matching records found.")
        else:
            await ctx.send("You do not have the required clearance to access personnel records.")

# Load the cog
def setup(bot):
    bot.add_cog(Personnel(bot))

