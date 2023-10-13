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

initial_extensions = ['cogs.ping', 'cogs.clear']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Online"))

# Load extensions (cogs)
if __name__ == '__cogs__':
    for extension in initial_extensions:
        asyncio.run(bot.load_extension(extension))

@bot.event
async def on_disconnect():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Under Maintenance"))
    channel = bot.get_channel(1162234055253835968)  # Replace with the desired channel ID
    if channel:
        await channel.send("Bot is undergoing maintenance and is now offline.")

@bot.event
async def on_connect():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Online"))
    channel = bot.get_channel(1162234055253835968)  # Replace with the desired channel ID
    if channel:
        await channel.send("Bot is back online and ready for action!")

# Read the bot token from the environment variable
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

bot.run(BOT_TOKEN)
