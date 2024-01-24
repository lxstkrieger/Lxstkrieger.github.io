import discord
from discord.ext import commands
from discord.commands import slash_command
import logging


class Clear(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="clears a channel with your amount")
    @commands.has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 1000):
        try:
            await ctx.channel.purge(limit=amount)
            clear_embed = discord.Embed(
                title=f"{amount} Messages got purged",
                description=f"This Message delete after 3 Seconds",
                color=discord.Color.magenta()
            )
            clear_embed.set_thumbnail(url="https://media4.giphy.com/media/jAYUbVXgESSti/giphy.gif?cid=ecf05e47wrxukzkng5pw6kule2v7lk64cnal1km55s8kw0dp&ep=v1_gifs_search&rid=giphy.gif&ct=g")
            clear_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=clear_embed, delete_after=3)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Clear(bot))
