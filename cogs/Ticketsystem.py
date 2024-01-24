import discord
from discord.ext import commands
from discord.commands import slash_command
import logging


class Ticketsystem(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    @slash_command(description="Create a new Ticket ")
    async def createticket(self, ctx):
        try:
            ticket_channel = await ctx.guild.create_text_channel(name=f"ticket-{ctx.author.display_name}")

            # Set permissions for the author
            await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True,
                                                 embed_links=True, attach_files=True, read_message_history=True,
                                                 external_emojis=True)

            # Set permissions for the Ticket-Helper role
            guild = ctx.guild
            rolesearch = discord.utils.get(guild.roles, name="🙋🏻‍♂️Support Team🙋🏻‍♂️")

            if rolesearch:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False),
                    ctx.author: discord.PermissionOverwrite(send_messages=True, read_messages=True),
                    rolesearch: discord.PermissionOverwrite(send_messages=True, read_messages=True, add_reactions=True,
                                                            embed_links=True, attach_files=True, read_message_history=True,
                                                            external_emojis=True, manage_channels=True)
                }

                await ticket_channel.edit(overwrites=overwrites)
                await ctx.respond(f"Your Ticket Channel was Created. here Your Ticket: {ticket_channel.mention}", ephemeral=True)
            else:
                await ctx.send(
                    "Error: Role '🙋🏻‍♂️Support Team🙋🏻‍♂️' not found. Please create the role before using the ticket system.")

            embed = discord.Embed(color=0xff8103)
            embed.add_field(name="Support Ticket", value=f"Ticket by {ctx.author.mention}", inline=False)
            embed.add_field(name="Option:", value=":lock: - ```/closeticket - <#ticket>```", inline=False)
            embed.set_footer(text=f"Ticket | {ctx.author}")
            await ticket_channel.send(embed=embed)
            await ticket_channel.send(
                f"Hello, {ctx.author.mention}! Please describe your problem as well as you can so that a 🙋🏻‍♂️Support Team🙋🏻‍♂️ can help you.")
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    @slash_command(description="Close a Ticket(Only Team Member can Use This!)")
    @commands.has_permissions(manage_channels=True)
    async def closeticket(self, ctx):
        try:
            await ctx.channel.delete()
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    @slash_command(description="Setup the Ticketsystem")
    @commands.has_permissions(administrator=True)
    async def setupticketsystem(self, ctx):
        try:
            await ctx.guild.create_role(name="🙋🏻‍♂️Support Team🙋🏻‍♂️", colour=discord.Colour(0xE03400))
            setup_embed = discord.Embed(title="Information",
                               description="Ticket System was successfully installed. | Attention If you run ```/setupticketsystem``` again, the ticket system will no longer work and report an error. Since there are there 2 roles of ticket helper you have to delete one then, This code is still in development for problems/questions contact me on Discord : Talha2018#0001",
                               color=0x00ff00)
            setup_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.send(embed=setup_embed)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(Ticketsystem(bot))
