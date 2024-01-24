import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import requests


class Dance(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="kiss someone...")
    async def dance(self, ctx):
        try:
            resp = requests.get("https://nekos.best/api/v2/dance")
            data = resp.json()
            image = data["results"][0]["url"]
            dance_embed = discord.Embed(
                color=discord.Color.magenta(),
                description=f"{ctx.author.mention} are dancing"
            )
            dance_embed.set_image(url=image)
            dance_embed.set_footer(text=f"Embed created from {self.bot.user}")

            await ctx.respond(embed=dance_embed)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Dance(bot))
