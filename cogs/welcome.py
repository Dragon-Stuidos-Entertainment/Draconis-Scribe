import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = 1162823959725740103  # Replace with the actual channel ID where you want to send the welcome message

        channel_to_read = "#enlist-now", "#how-to-join", "about-us"  # Replace with the actual channel name you want to mention

        channel = self.bot.get_channel(channel_id)

        if channel:
            # Create an embed for the welcome message
            embed = discord.Embed(title="Welcome to the Office of Naval Intelligence", color=discord.Color(0xFFFFFF))
            embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLg5IvbPpE5enQ-696wFW74R3pUfZw-Mp-yUyPk6vaGw&s")
            embed.description = f"Welcome, {member.mention}! Thank you for joining our server. Make sure you fill out an Application, to enlist with ONI. To do so, go to the {channel_to_read} channel and read the instructions on how to apply."

            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))
