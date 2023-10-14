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

            def check_reaction(reaction, user):
                return user == ctx.author and reaction.message.id == message.id

            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=300, check=check_reaction)
                if reaction.emoji == "✅":
                    # Approve the application
                    application["status"] = "Approved"
                    await dm_channel.send(f"Your application has been approved by {ctx.author.display_name}. Please provide a reason for approval.")
                elif reaction.emoji == "❌":
                    # Deny the application
                    application["status"] = "Denied"
                    await dm_channel.send(f"Your application has been denied by {ctx.author.display_name}. Please provide a reason for denial.")

            except asyncio.TimeoutError:
                await dm_channel.send("You took too long to react. The application status has been left pending.")
        else:
            await ctx.send("Enlistment channel not found. Please contact the server administrator.")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message is a response to an approved/denied application
        if message.author == self.bot.user:
            parts = message.content.split("Application for")
            if len(parts) == 2:
                user_id = parts[1].splitlines()[0].strip()
                application = self.applications.get(int(user_id))
                if application:
                    application["reason"] = parts[1].splitlines()[1].strip()
                    if "Approved" in application["status"]:
                        await self.send_approval_notification(application, message.author.display_name)
                    elif "Denied" in application["status"]:
                        await self.send_denial_notification(application, message.author.display_name)
                    del self.applications[int(user_id)]

    async def send_approval_notification(self, application, approver):
        # Send an approval notification to the applicant
        dm_channel = await self.bot.get_user(application["message"].author.id).create_dm()
        await dm_channel.send(f"Your application has been approved by {approver} with the following reason: {application['reason']}")

    async def send_denial_notification(self, application, denier):
        # Send a denial notification to the applicant
        dm_channel = await self.bot.get_user(application["message"].author.id).create_dm()
        await dm_channel.send(f"Your application has been denied by {denier} with the following reason: {application['reason']}")

def setup(bot):
    bot.add_cog(Enlistment(bot))
