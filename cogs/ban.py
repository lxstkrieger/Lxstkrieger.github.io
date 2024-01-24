import discord
from discord.ext import commands
from discord.commands import slash_command
import logging


class Ban(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="Ban a user")
    async def ban(self, ctx, member: discord.Member):
        try:
            if ctx.author.guild_permissions.ban_members:
                await ctx.guild.ban(member)
                ban_embed = discord.Embed(
                    color=discord.Color.red(),
                    description=f"{member.mention} got banned"
                )
                ban_embed.set_thumbnail(url=member.display_avatar)
                ban_embed.set_image(url="https://media1.giphy.com/media/hSXiJbWunRqZMr0KTE/giphy.gif?cid=ecf05e47c1tyzvsa9muz9l7y4m2hitfojqoqbjw8p393qcgk&ep=v1_gifs_search&rid=giphy.gif&ct=g")
                ban_embed.set_footer(text=f"Embed created from {self.bot.user}")
                await ctx.respond(embed=ban_embed, ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Ban(bot))
