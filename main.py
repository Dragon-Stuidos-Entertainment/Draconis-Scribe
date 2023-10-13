import os
import discord
from discord.ext import commands
import datetime
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Define your channel ID here
YOUR_CHANNEL_ID = 1162234055253835968  # Replace with your channel's actual ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Online"))

@bot.event
async def on_disconnect():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Under Maintenance"))
    channel = bot.get_channel(YOUR_CHANNEL_ID)
    if channel:
        await channel.send("Bot is undergoing maintenance and is now offline.")

@bot.event
async def on_connect():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Online"))
    channel = bot.get_channel(YOUR_CHANNEL_ID)
    if channel:
        await channel.send("Bot is back online and ready for action!")

# ... rest of your code ...

# Read the bot token from the environment variable
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

bot.run(BOT_TOKEN)
