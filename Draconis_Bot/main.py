import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
# Define log_channel_id as a global variable
log_channel_id = 1163150349511696484  # Update this with your actual log channel ID

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load all extensions (cogs) from the "cogs" directory
def load_extensions():
    loaded_cogs = []  # Create an empty list to store the names of loaded cogs
    for filename in os.listdir('Draconis_Bot/cogs'):
        if filename.endswith('.py'):
            cog_name = f'cogs.{filename[:-3]}'  # Generate the cog name
            bot.load_extension(cog_name)
            loaded_cogs.append(cog_name)  # Add the loaded cog name to the list
    # Print the loaded cogs
    print("Loaded cogs:", ", ".join(loaded_cogs))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id}')
    load_extensions()  # Load all extensions (cogs)

    channel = bot.get_channel(log_channel_id)
    if channel:
        await channel.send("Bot is online and ready for action!")

# Your other event functions and commands here

# Read the bot token from the environment variable
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if DISCORD_BOT_TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

bot.run(DISCORD_BOT_TOKEN)
