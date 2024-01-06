import discord
from discord.ext import commands

class UserReporting(commands.Cog):
    def __init__(self, bot, report_channel_id):
        self.bot = bot
        self.report_channel_id = report_channel_id

    @commands.command(name="report")
    async def report_user(self, ctx, user_id: int, reason: str, evidence: str = None):
        report_channel = self.bot.get_channel(self.report_channel_id)
        if report_channel:
            # Get the reported user
            reported_user = self.bot.get_user(user_id)

            if reported_user:
                report_message = f"Report from {ctx.author.mention}:\n"
                report_message += f"**Reported User:** {reported_user.mention}\n"
                report_message += f"**Reason:** {reason}\n"

                if evidence:
                    report_message += f"**Evidence/Details:** {evidence}\n"

                await report_channel.send(report_message)
                await ctx.message.delete()  # Delete the user's report command message
                await ctx.send("Thank you for your report. Our moderation team will review it.")
            else:
                await ctx.send("The reported user ID is not valid.")
        else:
            await ctx.send("Reporting channel not found. Please set up a valid reporting channel with the bot owner.")

def setup(bot):
    bot.add_cog(UserReporting(bot, 1163295665753948161))  # Use the provided REPORT_CHANNEL_ID
