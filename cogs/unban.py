import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import logging


class Unban(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(name="unban", description="unbans specified member.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, reason: Option(str, "Enter a reason for the unban", required=False, default='no reason given')):
        try:
            await ctx.guild.unban(user)
            unban_embed = discord.Embed(
                title="Success",
                description=f"{user.mention} has been unbanned.",
                color=discord.Color.green()
            )
            unban_embed.add_field(name="reason", value=reason)
            await ctx.response.send_message(embed=unban_embed, ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Unban(bot))
