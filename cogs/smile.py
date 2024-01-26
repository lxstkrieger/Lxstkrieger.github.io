import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import requests


class Smile(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="smileing")
    async def smile(self, ctx, member: discord.Member):
        try:
            resp = requests.get("https://nekos.best/api/v2/husbando")
            data = resp.json()
            image = data["results"][0]["url"]
            smile_embed = discord.Embed(
                color=discord.Color.magenta(),
                description=f"{ctx.author.mention} husbandoing {member.mention}"
            )
            smile_embed.set_image(url=image)
            smile_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=smile_embed)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Smile(bot))
