import discord
from datetime import datetime
from discord import Option
from discord.commands import slash_command
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import logging


class Unban(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="Get a list of members who are banned from this server!")
    @commands.has_permissions(ban_members=True)
    async def bans(self,ctx):
        try:
            await ctx.defer()
            embed = discord.Embed(title=f"List of Bans in {ctx.guild}", timestamp=datetime.now(),
                                  color=discord.Colour.red())
            async for entry in ctx.guild.bans():
                user = entry.user
                if len(embed.fields) >= 25:
                    break
                if len(embed) > 5900:
                    embed.add_field(name="Too many bans to list")
                else:
                    embed.add_field(name=f"Ban",
                                    value=f"Username: {entry.user.name}#{entry.user.discriminator}\nReason: {entry.reason}\nUser ID: {entry.user.id}\nIs Bot: {entry.user.bot}",
                                    inline=False)
            await ctx.respond(embed=embed)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    @bans.error
    async def banserror(self,ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You need ban members permissions to do this!")
        else:
            await ctx.respond(f"Something went wrong, I couldn't unban this member or this member isn't banned.")
            raise error


    @slash_command(description="Unbans a member")
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx, id: Option(discord.Member, description="The User ID of the person you want to unban.", required=True)):
        try:
            await ctx.defer()
            member = await self.bot.get_or_fetch_user(id)
            await ctx.guild.unban(member)
            await ctx.respond(f"I have unbanned {member.mention}.")
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    @unban.error
    async def unbanerror(self,ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You need ban members permissions to do this!")
        else:
            await ctx.respond(f"Something went wrong, I couldn't unban this member or this member isn't banned.")
            raise error


def setup(bot: discord.Bot):
    bot.add_cog(Unban(bot))