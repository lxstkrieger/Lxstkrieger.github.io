import discord
from datetime import datetime

from discord.commands import slash_command
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import logging


class Bans(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="Get a list of members who are banned from this server!")
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):
        try:
            await ctx.defer()
            bans_embed = discord.Embed(title=f"List of Bans in {ctx.guild}", timestamp=datetime.now(), color=discord.Colour.red())
            async for entry in ctx.guild.bans():
                if len(bans_embed.fields) >= 25:
                    break
                if len(bans_embed) > 5900:
                    bans_embed.add_field(name="Too many bans to list", value="", inline=True)
                else:
                    bans_embed.add_field(name=f"Ban", value=f"Username: {entry.user.name}#{entry.user.discriminator}\nReason: {entry.reason}\nUser ID: {entry.user.id}\nIs Bot: {entry.user.bot}", inline=False)
                    bans_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=bans_embed)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    @bans.error
    async def banserror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You need ban members permissions to do this!")
        else:
            await ctx.respond(f"Something went wrong, I couldn't unban this member or this member isn't banned.")
            raise error


def setup(bot: discord.Bot):
    bot.add_cog(Bans(bot))
