import discord
from discord.ext import commands

class Enlistment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # List of enlistment questions
        self.enlistment_questions = [
            "What is your full name?",
            "What is your age?",
            "Gamertag?",
            "What interests you about joining ONI?",
            "Do you have any previous experience?",
            "What skills can you bring to ONI?",
            "How did you hear about ONI?",
            "What time zone are you in?",
            "Are you comfortable with following orders?",
            "What are your goals within ONI?"
            "Give us a bit about yourself?"
        ]

    @commands.command(name="enlist")
    async def enlist(self, ctx):
        # Initialize answers
        answers = []

        # Send questions to the user in DMs
        for question in self.enlistment_questions:
            dm_channel = await ctx.author.create_dm()
            await dm_channel.send(question)
            try:
                response = await self.bot.wait_for('message', timeout=300, check=lambda m: m.author == ctx.author and m.channel == dm_channel)
                answers.append(response.content)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond. The enlistment process has been canceled.")
                return

        # Store or process answers as needed
        # In this example, we just print the answers
        for i, answer in enumerate(answers):
            await ctx.send(f"Question {i + 1}: Your answer - {answer}")

        # Send the answers to a specific channel
        enlistment_channel = self.bot.get_channel(YOUR_ENLISTMENT_CHANNEL_ID)  # Replace with the actual channel ID
        if enlistment_channel:
            # Format answers as a message
            answers_message = "\n".join([f"Question {i + 1}: {question}\nAnswer: {answer}" for i, (question, answer) in enumerate(zip(self.enlistment_questions, answers))])
            await enlistment_channel.send(f"New enlistment application from {ctx.author.mention}:\n{answers_message}")

def setup(bot):
    bot.add_cog(Enlistment(bot))
