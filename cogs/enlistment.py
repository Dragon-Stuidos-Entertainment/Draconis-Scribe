import discord
from discord.ext import commands

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
        application = {"questions": [], "answers": [], "status": None, "reason": None}

        # List of enlistment questions
        enlistment_questions = [
            "What is your full name?",
            "What is your age?",
            "Where are you from?",
            "What interests you about joining ONI?",
            "Do you have any previous experience relevant to ONI?",
            "What skills can you bring to ONI?",
            "How did you hear about ONI?",
            "What time zone are you in?",
            "Are you comfortable with following orders?",
            "Do you understand the confidentiality of ONI missions?"
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

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Check if the reaction was added to an enlistment application message
        if user.bot:
            return

        message = reaction.message
        if message.id in self.applications.values():
            # Check the reaction and user
            application = next((app for app in self.applications if self.applications[app]["message"] == message.id), None)

            if reaction.emoji == "✅":
                # Approve the application
                self.applications[application]["status"] = "Approved"

                # Ask for a reason for approval
                await message.clear_reactions()
                await message.edit(content=f"Application for {user.display_name} has been approved. Please provide a reason for approval.")
                try:
                    reason_response = await self.bot.wait_for('message', timeout=300, check=lambda m: m.author == user and m.channel == message.channel)
                    self.applications[application]["reason"] = reason_response.content
                except asyncio.TimeoutError:
                    self.applications[application]["reason"] = "No reason provided."

                # Notify the user
                await user.send(f"Your application has been approved with the following reason: {self.applications[application]['reason']}")
            elif reaction.emoji == "❌":
                # Deny the application
                self.applications[application]["status"] = "Denied"

                # Ask for a reason for denial
                await message.clear_reactions()
                await message.edit(content=f"Application for {user.display_name} has been denied. Please provide a reason for denial.")
                try:
                    reason_response = await self.bot.wait_for('message', timeout=300, check=lambda m: m.author == user and m.channel == message.channel)
                    self.applications[application]["reason"] = reason_response.content
                except asyncio.TimeoutError:
                    self.applications[application]["reason"] = "No reason provided."

                # Notify the user
                await user.send(f"Your application has been denied with the following reason: {self.applications[application]['reason']}")

def setup(bot):
    bot.add_cog(Enlistment(bot))
