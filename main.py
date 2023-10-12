import os
import discord
from decouple import config
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command()
async def who_are_you(ctx):
    await ctx.send("I am Blackbox, the Office of Naval Intelligence AI. How may I help you?")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I'm your Discord bot!")

@bot.command()
async def ping(ctx):
    # Calculate the response time (latency) of the bot
    before = datetime.datetime.now()
    message = await ctx.send("Pinging...")
    after = datetime.datetime.now()
    latency = (after - before).total_seconds() * 1000

    # Edit the message to show the latency
    await message.edit(content=f"Pong! Latency is {latency:.2f}ms")

@bot.event
async def on_message(message):
    if message.content.lower() == "who are you":
        response = "I am Blackbox, the Office of Naval Intelligence AI. How may I help you?"
        await message.channel.send(response)

    await bot.process_commands(message)

# Read the bot token from the environment variable
BOT_TOKEN = config ('TOKEN')

bot.run(BOT_TOKEN)