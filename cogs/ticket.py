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

        # Send an initial message to the user
        await user_ticket.send(f"Hello {ctx.author.mention}, an Officer will be with you shortly.")

        await ctx.send(f"Your support ticket has been created in {user_ticket.mention}. Please describe your issue.")

    @commands.command(name="close_ticket")
    async def close_ticket(self, ctx):
        # Check if the user has a ticket
        user_ticket = discord.utils.get(ctx.guild.text_channels, name=f"ticket-{ctx.author.id}")

        if not user_ticket:
            await ctx.send("You don't have an open ticket to close.")
            return

        # Send a copy of the closed ticket to an admin channel (replace with your channel ID)
        admin_channel = ctx.guild.get_channel(1163145966682128486)  # Replace with your admin channel ID

        if admin_channel:
            await admin_channel.send(f"Closed Ticket - {user_ticket.name}")
            async for message in user_ticket.history():
                await admin_channel.send(f"{message.author.display_name}: {message.content}")

        # Delete the user's ticket channel
        await user_ticket.delete()
        await ctx.send("Your ticket has been closed. If you have more questions, feel free to create a new one.")

def setup(bot):
    bot.add_cog(Ticket(bot))
