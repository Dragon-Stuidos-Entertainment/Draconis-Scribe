import discord
from discord.ext import commands

def has_add_role_permission(ctx):
    return ctx.author.guild_permissions.manage_roles

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    @commands.command()
    @commands.check(has_add_role_permission)
    async def addrole(self, ctx, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await ctx.author.add_roles(role)
            await ctx.send(f'You have been given the "{role_name}" role.')
        else:
            await ctx.send(f'The role "{role_name}" does not exist.')

    @commands.command()
    @commands.check(has_add_role_permission)
    async def removerole(self, ctx, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await ctx.author.remove_roles(role)
            await ctx.send(f'You no longer have the "{role_name}" role.')
        else:
            await ctx.send(f'The role "{role_name}" does not exist.')

def setup(bot):
    bot.add_cog(RoleManagement(bot))
