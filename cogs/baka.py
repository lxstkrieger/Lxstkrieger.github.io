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
    async def kiss(self, ctx, member: discord.Member):

        resp = requests.get("https://nekos.best/api/v2/baka")
        data = resp.json()
        image = data["results"][0]["url"]
        kiss_embed = discord.Embed(
            color=discord.Color.magenta(),
            description=f"{member.mention} is a BAKA BAKA BAKA BAKA !!!!"
        )
        kiss_embed.set_image(url=image)
        await ctx.respond(embed=kiss_embed)



def setup(bot: discord.Bot):
    bot.add_cog(Baka(bot))