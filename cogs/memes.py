import discord
from discord.ext import commands,tasks
from discord.commands import slash_command
import requests

class Memes(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description='sends a meme')
    async def meme(self,ctx):
        # Make a request to the meme API
        meme_response = requests.get('https://meme-api.com/gimme')

        if meme_response.status_code == 200:
            meme_data = meme_response.json()
            meme_url = meme_data.get('url')
            await ctx.respond(f'Here is a meme for you: {meme_url}')
        else:
            await ctx.send('Error fetching meme.')


def setup(bot: discord.Bot):
    bot.add_cog(Memes(bot))