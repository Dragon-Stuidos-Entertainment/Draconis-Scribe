import os
import discord
from discord.ext import commands

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
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    load_extensions()  # Load all extensions (cogs)
    
    # Replace this with your channel ID
    your_channel_id = 1162892621895696394
    
    channel = bot.get_channel(your_channel_id)
    if channel:
        await channel.send("Bot is online and ready for action!")

@bot.event
async def on_disconnect():
    # Replace this with your channel ID
    your_channel_id = 1162892621895696394
    
    channel = bot.get_channel(your_channel_id)
    if channel:
        await channel.send("Bot is undergoing maintenance and is now offline.")

@bot.command(name="help")
async def help_command(ctx, command_name: str = None):
    if not command_name:
        # If no specific command is specified, list all available commands
        embed = discord.Embed(title="Command List", color=discord.Color.blue())
        for cog in bot.cogs:
            commands_list = bot.get_cog(cog).get_commands()
            if commands_list:
                command_names = [command.name for command in commands_list]
                embed.add_field(name=cog, value=" | ".join(command_names), inline=False)
        await ctx.send(embed=embed)
    else:
        # If a specific command is specified, provide information about that command
        command = bot.get_command(command_name)
        if not command:
            await ctx.send("Command not found.")
        else:
            embed = discord.Embed(title=f"Help: {command.name}", description=command.help, color=discord.Color.blue())
            await ctx.send(embed=embed)

# Your other event functions and commands here

# Read the bot token from the environment variable
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

bot.run(BOT_TOKEN)
