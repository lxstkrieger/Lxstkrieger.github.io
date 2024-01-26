import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import requests


class Yeet(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="someone yeet's you")
    async def yeet(self, ctx, member: discord.Member):
        try:
            resp = requests.get("https://nekos.best/api/v2/yeet")
            data = resp.json()
            image = data["results"][0]["url"]
            yeet_embed = discord.Embed(
                color=discord.Color.magenta(),
                description=f"{ctx.author.mention} yeet's {member.mention}"
            )
            yeet_embed.set_image(url=image)
            yeet_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=yeet_embed)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Yeet(bot))
