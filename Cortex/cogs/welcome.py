import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = 1220912889376804977  # Replace with the actual channel ID where you want to send the welcome message

        welcome_channel = self.bot.get_channel(channel_id)

        if welcome_channel:
            # Create an embed for the welcome message
            embed = discord.Embed(color=discord.Color.purple())  # Using purple for a vibrant, creative feel

            # Embed author set to Dragon Studios Entertainment
            embed.set_author(name="Dragon Studios Entertainment", icon_url="https://example.com/dragon_studios_logo.png")  # Replace the URL with your studio's logo

            # Simplified welcome message without mentioning an avatar
            embed.description = (f"🐉 Welcome to Autumn's Contigency, {member.mention} We welcome you aboard our ship are you here to join us, are you a member of a allied force, or are you simply a guest? Let the staff of the Autumn know so we can provide you with proper access. 🌟\n\n" "We look forward to seeing you around.")

            # Optional: Add a footer and timestamp for a personal touch
            embed.set_footer(text="Welcome Committee • Dragon Studios Entertainment")
            embed.timestamp = discord.utils.utcnow()

            await welcome_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))
