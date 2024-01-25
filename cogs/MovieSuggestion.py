import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import requests


class MovieSuggestion(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    # TODO: COMMAND SCHREIBEN FÜR FILM UND SERIEN VORSCHLAG JE NACH GENRE ETC.


def setup(bot: discord.Bot):
    bot.add_cog(MovieSuggestion(bot))
