import discord
from discord.ext import commands
import requests

class Askbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "API_KEY"  # Replace with your OpenAI API key

    @commands.command()
    async def askbot(self, ctx, *, question):
        # Define the OpenAI API endpoint
        endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"

        # Set up the headers for the API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Set up the data for the API request
        data = {
            "prompt": question,
            "max_tokens": 100,  # Adjust this to limit the response length
        }

        # Make the API request
        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["text"]
            await ctx.send(answer)
        else:
            await ctx.send("An error occurred while fetching the response from ChatGPT. Please try again later.")

def setup(bot):
    bot.add_cog(Askbot(bot))
