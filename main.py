import os
import discord
from discord.ext import commands
import datetime
import asyncio  # Import the asyncio module

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    # Set the initial presence
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Under Maintenance"))

@bot.command()
async def whoareyou(ctx):
    await ctx.send("I am Blackbox, the Office of Naval Intelligence AI. How may I help you?")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I'm your Discord bot!")

@bot.command()
async def ping(ctx):
    before = datetime.datetime.now()
    message = await ctx.send("Pinging...")
    after = datetime.datetime.now()
    latency = (after - before).total_seconds() * 1000
    await message.edit(content=f"Pong! Latency is {latency:.2f}ms")

@bot.command()
async def clear(ctx, amount=5):
    if ctx.message.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
    else:
        await ctx.send("You don't have permission to manage messages.")

@bot.event
async def on_message(message):
    if message.content.lower() == "who are you":
        response = "I am Blackbox, the Office of Naval Intelligence AI. How may I help you?"
        await message.channel.send(response)

    await bot.process_commands(message)

# Read the bot token from the environment variable
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

bot.run(BOT_TOKEN)
