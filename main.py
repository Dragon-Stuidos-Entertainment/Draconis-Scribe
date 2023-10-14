import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load all extensions (cogs) from the "cogs" directory

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.load_extension("cogs.ping")
    await bot.load_extension("cogs.clear")

# Your other event functions and commands here

# Read the bot token from the environment variable
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

bot.run(BOT_TOKEN)
