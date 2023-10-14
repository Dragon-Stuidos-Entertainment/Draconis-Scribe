import discord
from discord.ext import commands

def has_add_role_permission(ctx):
    return ctx.author.guild_permissions.manage_roles

def is_bot_command(ctx):
    return ctx.author.bot

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    @commands.command()
    @commands.check(has_add_role_permission)
    async def addrole(self, ctx, role_name: str, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await user.add_roles(role)
            await ctx.send(f'{user.mention} has been given the "{role_name}" role.')
        else:
            await ctx.send(f'The role "{role_name}" does not exist.')

    @commands.command()
    @commands.check(has_add_role_permission)
    async def removerole(self, ctx, role_name: str, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await user.remove_roles(role)
            await ctx.send(f'{user.mention} no longer has the "{role_name}" role.')
        else:
            await ctx.send(f'The role "{role_name}" does not exist.')

    @commands.command()
    @commands.check(has_add_role_permission)
    async def createrole(self, ctx, role_name: str, role_color: discord.Color = discord.Color.default()):
        # Create a new role with the specified name and color
        await ctx.guild.create_role(name=role_name, color=role_color)
        await ctx.send(f'The role "{role_name}" has been created.')

        # Delete the command message
        await ctx.message.delete()

    @commands.command()
    @commands.check(is_bot_command)
    async def deletemycommand(self, ctx):
        # Delete the bot's command message
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(RoleManagement(bot))
