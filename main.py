@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    load_extensions()  # Load all extensions (cogs)
    
    # Replace this with your server (guild) ID
    your_guild_id = 1118420639947173959
    
    guild = bot.get_guild(your_guild_id)
    if guild:
        # Replace this with your desired channel name
        channel_name = "bot-status"
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if channel:
            await channel.send("Authorization Granted Bot is online")

@bot.event
async def on_disconnect():
    # Replace this with your server (guild) ID
    your_guild_id = 123456789012345678
    
    guild = bot.get_guild(your_guild_id)
    if guild:
        # Replace this with your desired channel name
        channel_name = "bot-status"
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if channel:
            await channel.send("Bot is undergoing maintenance and is now offline.")
