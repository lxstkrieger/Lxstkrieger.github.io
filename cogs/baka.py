import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import requests


class Baka(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="kiss someone...")
    async def baka(self, ctx, member: discord.Member):

        resp = requests.get("https://nekos.best/api/v2/baka")
        data = resp.json()
        image = data["results"][0]["url"]
        baka_embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"{member.mention} is a BAKA BAKA BAKA BAKA !!!!"
        )
        baka_embed.set_image(url=image)
        baka_embed.set_footer(text=f"Embed created from {self.bot.user}")
        await ctx.respond(embed=baka_embed)


def setup(bot: discord.Bot):
    bot.add_cog(Baka(bot))
