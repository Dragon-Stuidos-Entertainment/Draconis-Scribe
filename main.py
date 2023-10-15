import os
import discord
from discord.ext import commands
from moderation_logger import ModerationLogger  # Import the ModerationLogger

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load all extensions (cogs) from the "cogs" directory
def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id}')
    load_extensions()  # Load all extensions (cogs)

    log_channel_id = 1163150349511696484  # Replace with your log channel ID
    logger = ModerationLogger(bot, log_channel_id)  # Create an instance of ModerationLogger

    bot.add_cog(logger)  # Add the ModerationLogger cog to the bot

    # Replace this with your channel ID
    your_channel_id = 1162892621895696394

    channel = bot.get_channel(your_channel_id)
    if channel:
        await channel.send("Bot is online and ready for action!")

# Your other event functions and commands here

# Read the bot token from the environment variable
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

bot.run(BOT_TOKEN)
