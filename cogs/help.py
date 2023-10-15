import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx, command_name: str = None):
        if not command_name:
            # If no specific command is specified, list all available commands
            embed = discord.Embed(title="Command List", color=discord.Color.blue())
            for cog in self.bot.cogs:
                commands_list = self.bot.get_cog(cog).get_commands()
                if commands_list:
                    command_names = [command.name for command in commands_list]
                    embed.add_field(name=cog, value=" | ".join(command_names), inline=False)
            await ctx.send(embed=embed)
        else:
            # If a specific command is specified, provide information about that command
            command = self.bot.get_command(command_name)
            if not command:
                await ctx.send("Command not found.")
            else:
                embed = discord.Embed(title=f"Help: {command.name}", description=command.help, color=discord.Color.blue())
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
