import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import requests


class SteamNews(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    # TODO: Steamworks SDK und Steamworks Web API nutzen um die Steam News zu bekommen dafür gehst du auf die Steam seite und holst dir API-KEY und APP-ID


def setup(bot: discord.Bot):
    bot.add_cog(SteamNews(bot))
