import discord
from discord.ext import commands
import asyncio

YOUR_ENLISTMENT_ID = 1162833977132982302

class Enlistment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Dictionary to store enlistment applications
        self.applications = {}

    @commands.command(name="enlist")
    async def enlist(self, ctx):
        # Check if the user has an existing application
        if ctx.author.id in self.applications:
            await ctx.send("You already have an existing application in progress.")
            return

        # Create a new enlistment application
        application = {"questions": [], "answers": [], "status": None, "reason": None, "approver": None}

        # List of enlistment questions
        enlistment_questions = [
            "What is your full name?",
            "What is your age?",
            "Gamertag?",
            "What interests you about joining ONI?",
            "Do you have any previous experience?",
            "What skills can you bring to ONI?",
            "How did you hear about ONI?",
            "What time zone are you in?",
            "Previous Clans?",
            "What are your goals?",
            "Motivation in being a part of a clan?",
            "How active can you be?"
        ]

        # Send questions to the user in DMs
        dm_channel = await ctx.author.create_dm()
        for question in enlistment_questions:
            await dm_channel.send(question)
            try:
                response = await self.bot.wait_for('message', timeout=300, check=lambda m: m.author == ctx.author and m.channel == dm_channel)
                application["questions"].append(question)
                application["answers"].append(response.content)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond. The enlistment process has been canceled.")
                return

        # Send the application to a specific channel for review
        enlistment_channel = self.bot.get_channel(YOUR_ENLISTMENT_ID)  # Replace with the actual channel ID
        if enlistment_channel:
            # Create an embed for the application
            embed = discord.Embed(title="Enlistment Application", color=discord.Color.blue())
            for question, answer in zip(application["questions"], application["answers"]):
                embed.add_field(name=question, value=answer, inline=False)
            embed.set_footer(text=f"Submitted by {ctx.author.display_name}")

            # Send the application as an embed
            message = await enlistment_channel.send(embed=embed)
            application["message"] = message.id
            self.applications[ctx.author.id] = application

            # Add reactions for approval and denial
            await message.add_reaction("✅")  # Approve
            await message.add_reaction("❌")  # Deny

            def check_reaction(reaction, reactor):
                return reactor != ctx.author and reaction.message.id == message.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=300, check=check_reaction)
                if reaction.emoji == "✅":
                    # Approve the application
                    application["status"] = "Approved"
                    application["approver"] = reaction.message.guild.get_member(user.id)
                    await dm_channel.send(f"Your application has been approved by {application['approver'].mention}. Congratulations!")
                elif reaction.emoji == "❌":
                    # Deny the application
                    application["status"] = "Denied"
                    application["approver"] = reaction.message.guild.get_member(user.id)
                    await dm_channel.send(f"Your application has been denied by {application['approver'].mention}. We appreciate your interest!")

            except asyncio.TimeoutError:
                await dm_channel.send("You took too long to react. The application status has been left pending.")
        else:
            await ctx.send("Enlistment channel not found. Please contact the server administrator.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return  # Ignore reactions by the bot

        if not reaction.message.embeds or not reaction.message.embeds[0].footer:
            return  # No embeds or footer in the message

        user_id = reaction.message.embeds[0].footer.text.split("Submitted by ")[1]
        application = self.applications.get(user_id)
        if application:
            if reaction.emoji == "✅":
                # Approve the application
                application["status"] = "Approved"
                application["approver"] = reaction.message.guild.get_member(user.id)
                await reaction.message.channel.send(f"Application for {user.mention} by {application['approver'].mention} has been approved. Congratulations, you have been approved!")
            elif reaction.emoji == "❌":
                # Deny the application
                application["status"] = "Denied"
                application["approver"] = reaction.message.guild.get_member(user.id)
                await reaction.message.channel.send(f"Application for {user.mention} by {application['approver'].mention} has been denied. We appreciate your interest!")

        self.applications[user_id] = application

    async def send_approval_notification(self, application):
        # Send an approval notification to the applicant
        dm_channel = await self.bot.get_user(application["message"].author.id).create_dm()
        await dm_channel.send(f"Your application has been approved by {application['approver'].mention}. Congratulations!")

    async def send_denial_notification(self, application):
        # Send a denial notification to the applicant
        dm_channel = await self.bot.get_user(application["message"].author.id).create_dm()
        await dm_channel.send(f"Your application has been denied by {application['approver'].mention}. We appreciate your interest!")

def setup(bot):
    bot.add_cog(Enlistment(bot))
