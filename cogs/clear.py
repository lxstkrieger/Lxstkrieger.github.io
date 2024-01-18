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
            await ctx.respond(f"{amount} Messages got purged.This message delete after 5 Seconds", delete_after=5)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Clear(bot))
