import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = 1188687484654190696  # Replace with the actual channel ID where you want to send the welcome message

        channel_to_read = "#enlist-now"  # Replace with the actual channel name you want to mention

        channel = self.bot.get_channel(channel_id)

        if channel:
            # Create an embed for the welcome message
            embed = discord.Embed(color=discord.Color(0x00FF00))  # Green color for transmission

            # Set the user's profile picture as the thumbnail
            embed.set_thumbnail(url=member.avatar_url)

            embed.set_author(name="Office of Naval Intelligence", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLg5IvbPpE5enQ-696wFW74R3pUfZw-Mp-yUyPk6vaGw&s")
            embed.description = f"Transmission incoming...\n\n**Welcome, {member.mention}!**\n\nThank you for joining our server. Make sure you fill out an Application, to enlist with UNSC Texas. To do so, go to the {channel_to_read} channel and read the instructions on how to apply.\n\n We look forward to seeing you on the field."

            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))
