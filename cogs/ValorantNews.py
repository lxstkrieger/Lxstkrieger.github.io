import discord
from discord.ext import commands, tasks
import requests


class ValorantNews(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.API_URL = 'https://vlrggapi.vercel.app/news'

        # TODO: VALORANT NEWS COMMAND


def setup(bot: discord.Bot):
    bot.add_cog(ValorantNews(bot))
