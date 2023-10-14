import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # This function will be called when a new member joins the server
        channel_id = 1234567890  # Replace with the actual channel ID where you want to send the welcome message

        # Get the channel by ID
        channel = self.bot.get_channel(channel_id)

        if channel:
            # Create an embed for the welcome message
            embed = discord.Embed(title="Welcome to the Office of Naval Intelligence", color=discord.Color(0xFFFFFF))  # White color
            embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLg5IvbPpE5enQ-696wFW74R3pUfZw-Mp-yUyPk6vaGw&s")  # Replace with the URL of the ONI logo image
            embed.description = f"Welcome, {member.mention}! Thank you for joining our server. Make sure you fill out a Application, to enlist with ONI. to do so go to the enlist-now channel, and read the ways to apply."

            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))
