import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import requests


class Stare(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="staring")
    async def stare(self, ctx, member: discord.Member):
        try:
            resp = requests.get("https://nekos.best/api/v2/stare")
            data = resp.json()
            image = data["results"][0]["url"]
            stare_embed = discord.Embed(
                color=discord.Color.magenta(),
                description=f"{ctx.author.mention} is staring at {member.mention}"
            )
            stare_embed.set_image(url=image)
            stare_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=stare_embed)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Stare(bot))
