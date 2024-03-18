import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = 1179244527987466250  # Replace with the actual channel ID where you want to send the welcome message

        welcome_channel = self.bot.get_channel(channel_id)

        if welcome_channel:
            # Create an embed for the welcome message
            embed = discord.Embed(color=discord.Color.purple())  # Using purple for a vibrant, creative feel

            # Embed author set to Dragon Studios Entertainment
            embed.set_author(name="Dragon Studios Entertainment", icon_url="https://example.com/dragon_studios_logo.png")  # Replace the URL with your studio's logo

            # Simplified welcome message without mentioning an avatar
            embed.description = (f"🐉 Welcome to Dragon Studios Entertainment, {member.mention}! 🌟\n\n"
                                 "We're thrilled to have you join our community of gamers, creators, and enthusiasts. "
                                 "Dive into our channels to chat, share, and explore everything we have to offer. "
                                 "Don't forget to check out our rules and announcements to get started on your adventure with us!\n\n"
                                 "Let the magic begin!")

            # Optional: Add a footer and timestamp for a personal touch
            embed.set_footer(text="Welcome Committee • Dragon Studios Entertainment")
            embed.timestamp = discord.utils.utcnow()

            await welcome_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))
