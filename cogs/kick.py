import discord
from discord.ext import commands
from discord.commands import slash_command
import logging


class Kick(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="Kick a user")
    async def kick(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.ban_members:
            await ctx.guild.kick(member)
            kick_embed = discord.Embed(
                color=discord.Color.red(),
                description=f"{member.mention} got kicked"
            )
            kick_embed.set_thumbnail(url=member.display_avatar)
            kick_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=kick_embed, ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(Kick(bot))
