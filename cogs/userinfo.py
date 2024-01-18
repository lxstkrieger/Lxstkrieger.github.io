import discord
from discord.ext import commands
from discord.commands import slash_command
import logging


class Userinfo(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="shows info from a specific user")
    async def userinfo(self, ctx, member: discord.Member):
        try:
            userinfo_embed = discord.Embed(
                title="Userinfo for",
                description=f"{member.mention}",
                color=discord.Color.blurple()
            )
            userinfo_embed.add_field(name="Server Joined at", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            userinfo_embed.add_field(name="Highest role", value=f"{member.top_role.mention}", inline=True)
            userinfo_embed.set_thumbnail(url=member.avatar)
            await ctx.respond(embed=userinfo_embed, ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Userinfo(bot))
