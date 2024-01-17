import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.ext.pages import Paginator,Page
import logging


class Help(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="help command")
    async def help(self,ctx):
        try:
            my_pages = [
                Page(
                    embeds=[
                        discord.Embed(
                            title="Moderation commands",
                            color=discord.Color.magenta(),
                        ).add_field(name="kick command", value=" kick's a User  ``` /kick <@Member>```", inline=False)
                        .add_field(name="ban command", value=" ban's a User  ``` /ban <@Member>```", inline=False)
                        .add_field(name="bans command", value=" shows banned Users  ``` /bans```", inline=False)
                        .add_field(name="unban command", value=" unban's a User  ``` /unban <@Member> or <MemberID>```",inline=False)
                        .add_field(name="timout command",value=" timeout's a User  ``` /timeout <@Member> <Duration in Seconds>```", inline=False)
                        .set_thumbnail(url=ctx.guild.icon)

                    ],
                ),
                Page(
                    embeds=[
                        discord.Embed(title="Warnsystem Commands",
                                      color=discord.Color.magenta(),
                                      description="Moderator Only commands"
                                      ).add_field(name="Warn Command", value=" Warn a User  ``` /warn <@Member>```",inline=False)
                                       .add_field(name="Warnings Command", value=" Shows Warns from a Specific User  ``` /warnings <@Member>```", inline=False)
                                       .add_field(name="Unwarn Command", value=" Unwarn's a Specific User(delete last given warn)  ``` /unwarn <@Member>```",inline=False)
                                       .set_thumbnail(url=ctx.guild.icon)
                    ],
                ),
                Page(
                    embeds=[
                        discord.Embed(title="Fun Commands",
                                      color=discord.Color.magenta(),
                                      ).add_field(name="baka command", value=" A User is a BAKA  ``` /baka <@Member>```",
                                                  inline=False)
                        .add_field(name="hug command", value=" Hug a User  ``` /hug <@Member>```", inline=False)
                        .add_field(name="punch command", value=" Punch a User  ``` /punch <@Member>```", inline=False)
                        .add_field(name="kiss command", value=" Kiss a User  ``` /kiss <@Member>```", inline=False)
                        .set_thumbnail(url=ctx.guild.icon)
                    ],
                ),

                Page(
                    embeds=[
                        discord.Embed(title="Ticketsystem Commands",
                                      color=discord.Color.magenta(),
                                      ).add_field(name="create Ticket command",
                                                  value=" Create a Ticket  ``` /createticket```", inline=False)
                        .add_field(name="close Ticket command",value=" Close a Ticket(Moderator Only)  ``` /closeticket```", inline=False)
                        .add_field(name="Setup Ticketsystem command", value=" Setup Ticketsystem(Administrator Only)  ``` /setupticketsystem```", inline=False)
                        .set_thumbnail(url=ctx.guild.icon)

                    ],
                ),
                Page(
                    embeds=[
                        discord.Embed(title="Levelsystem Commands",
                                      color=discord.Color.magenta(),
                                      ).add_field(name="Rank Command",value=" Show's Rank from a User  ``` /rank <@Member>```", inline=False)
                                       .add_field(name="Leaderboard Command", value=" Show's the Server Leaderboard  ``` /leaderboard ```",inline=False)
                                       .set_thumbnail(url=ctx.guild.icon)

                    ],
                ),
                Page(
                    embeds=[
                        discord.Embed(title="TempVoice Commands",
                                      color=discord.Color.magenta(),
                                      ).add_field(name="Lock Voice Command",value=" Locking the Voice Channel  ``` /lock```", inline=False)
                                       .set_thumbnail(url=ctx.guild.icon)
                    ],
                ),
            ]

            paginator = Paginator(pages=my_pages)
            await paginator.respond(ctx.interaction, ephemeral=True)

        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

def setup(bot: discord.Bot):
    bot.add_cog(Help(bot))