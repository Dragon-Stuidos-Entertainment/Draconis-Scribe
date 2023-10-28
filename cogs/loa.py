import discord
from discord.ext import commands
import asyncio

YOUR_LOA_CHANNEL_ID = 1234567890  # Replace with the actual channel ID where LOA requests should be sent

class LOA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Dictionary to store LOA requests
        self.loa_requests = {}

    @commands.command(name="loa")
    async def request_loa(self, ctx, *, reason):
        # Check if the user has an existing LOA request
        if ctx.author.id in self.loa_requests:
            await ctx.send("You already have an existing LOA request in progress.")
            return

        # Create a new LOA request
        loa_request = {"reason": reason, "status": "Pending", "approver": None}

        # Send the LOA request to a specific channel for review
        loa_channel = self.bot.get_channel(YOUR_LOA_CHANNEL_ID)
        if loa_channel:
            # Create an embed for the LOA request
            embed = discord.Embed(title="Leave of Absence Request", color=discord.Color.blue())
            embed.add_field(name="User", value=ctx.author.mention, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)

            # Send the request as an embed
            message = await loa_channel.send(embed=embed)
            loa_request["message"] = message.id
            self.loa_requests[ctx.author.id] = loa_request

            # Add reactions for approval and denial
            await message.add_reaction("✅")  # Approve
            await message.add_reaction("❌")  # Deny

            def check_reaction(reaction, reactor):
                return reactor != ctx.author and reaction.message.id == message.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=300, check=check_reaction)
                if reaction.emoji == "✅":
                    # Approve the LOA request
                    loa_request["status"] = "Approved"
                    loa_request["approver"] = reaction.message.guild.get_member(user.id)
                    await ctx.send(f"Your LOA request has been approved by {loa_request['approver'].mention}. Enjoy your leave!")
                elif reaction.emoji == "❌":
                    # Deny the LOA request
                    loa_request["status"] = "Denied"
                    loa_request["approver"] = reaction.message.guild.get_member(user.id)
                    await ctx.send(f"Your LOA request has been denied by {loa_request['approver'].mention}. Please contact an admin for more information.")

            except asyncio.TimeoutError:
                await ctx.send("You took too long to react. The LOA request status has been left pending.")
        else:
            await ctx.send("LOA channel not found. Please contact the server administrator.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return  # Ignore reactions by the bot

        if not reaction.message.embeds or not reaction.message.embeds[0].fields:
            return  # No embeds or fields in the message

        user_id = reaction.message.embeds[0].fields[0].value.split("User")[1].strip()
        loa_request = self.loa_requests.get(user_id)
        if loa_request:
            if reaction.emoji == "✅":
                # Approve the LOA request
                loa_request["status"] = "Approved"
                loa_request["approver"] = reaction.message.guild.get_member(user.id)
                await reaction.message.channel.send(f"LOA request for {user.mention} has been approved by {loa_request['approver'].mention}. Enjoy your leave!")
            elif reaction.emoji == "❌":
                # Deny the LOA request
                loa_request["status"] = "Denied"
                loa_request["approver"] = reaction.message.guild.get_member(user.id)
                await reaction.message.channel.send(f"LOA request for {user.mention} has been denied by {loa_request['approver'].mention}. Please contact an admin for more information.")

        self.loa_requests[user_id] = loa_request

def setup(bot):
    bot.add_cog(LOA(bot))
