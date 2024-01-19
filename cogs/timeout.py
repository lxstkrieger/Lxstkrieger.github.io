import discord
from discord.ext import commands
from discord.commands import slash_command
import logging
import datetime
from datetime import datetime
import humanfriendly


class Timeout(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command()
    @commands.has_permissions(ban_members=True)
    async def timeout(self, ctx, member: discord.Member, time=None, reason=None):
        try:
            time = humanfriendly.parse_timespan(time)
            await member.timeout(until=discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)
            await ctx.send(f"{member} was put into timeout for {time}")
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Timeout(bot))
