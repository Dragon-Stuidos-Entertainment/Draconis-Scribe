import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Define the load_extensions function before calling it
def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

# Your event decorators go here
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    load_extensions()  # Load all extensions (cogs)

    # Replace this with your channel ID
    your_channel_id = 1118420639947173959

    channel = bot.get_channel(your_channel_id)
    if channel:
        await channel.send("Bot is online and ready for action!")

@bot.event
async def on_disconnect():
    # Replace this with your channel ID
    your_channel_id = 1118420639947173959

    channel = bot.get_channel(your_channel_id)
    if channel:
        await channel.send("Bot is undergoing maintenance and is now offline.")

# Your other event functions and commands here

# Read the bot token from the environment variable
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

bot.run(BOT_TOKEN)
