import discord
from discord.ext import commands

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create_ticket")
    async def create_ticket(self, ctx):
        # Check if the user already has a ticket
        user_ticket = discord.utils.get(ctx.guild.text_channels, name=f"ticket-{ctx.author.id}")

        if user_ticket:
            await ctx.send("You already have an open ticket.")
            return

        # Create a new ticket channel
        category = discord.utils.get(ctx.guild.categories, name="Tickets")

        if not category:
            # If the "Tickets" category doesn't exist, create it
            category = await ctx.guild.create_category("Tickets")

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            category.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        user_ticket = await category.create_text_channel(f"ticket-{ctx.author.id}", overwrites=overwrites)

        await ctx.send(f"Your support ticket has been created in {user_ticket.mention}. Please describe your issue.")

    # You can add more commands for managing and interacting with tickets here

def setup(bot):
    bot.add_cog(Ticket(bot))
