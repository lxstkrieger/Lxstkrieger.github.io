import discord
from discord.ext import commands
from discord.commands import slash_command
import sqlite3
import os
import logging


class WarnSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB_path = os.path.abspath("C:/Users/Olive/Documents/DiscordBot/databases")
        db_file = os.path.join(self.DB_path, 'Warnsystem.db')
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    def create_table(self):
        # Create the warnings table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS warnings (
                            guild_id INTEGER,
                            user_id INTEGER,
                            reason TEXT)''')
        self.conn.commit()

    def add_warning(self, guild_id, user_id, reason):
        # Add a warning to the database
        self.cursor.execute("INSERT INTO warnings VALUES (?, ?, ?)", (guild_id, user_id, reason))
        self.conn.commit()

    def get_warnings(self, guild_id, user_id):
        # Get all warnings for a user in a guild
        self.cursor.execute("SELECT reason FROM warnings WHERE guild_id=? AND user_id=?", (guild_id, user_id))
        return self.cursor.fetchall()

    def remove_last_warning(self, guild_id, user_id):
        # Remove the last warning for a user in a guild
        self.cursor.execute("""
            DELETE FROM warnings
            WHERE rowid IN (
                SELECT rowid
                FROM warnings
                WHERE guild_id=? AND user_id=?
                ORDER BY rowid DESC
                LIMIT 1
            )
        """, (guild_id, user_id))
        self.conn.commit()

    @slash_command(description='warn a user')
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        try:
            self.add_warning(ctx.guild.id, member.id, reason)
            warn_embed= discord.Embed(color=discord.Color.red(),
                                      description=f"{member.mention} has been warned for: {reason}")
            warn_embed.set_thumbnail(url=member.display_avatar)
            warn_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=warn_embed,ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    @slash_command(description="show warns from a specific user")
    async def warnings(self, ctx, member: discord.Member):
        try:
            warns = self.get_warnings(ctx.guild.id, member.id)
            if warns:
                formatted_warns = [f"{idx + 1}. {warn[0]}" for idx, warn in enumerate(warns)]
                warnings_embed = discord.Embed(color=discord.Color.blue(),
                                               description=f"{member.mention} has the following warnings:\n" + "\n".join(formatted_warns))
                warnings_embed.set_thumbnail(url=member.display_avatar)
                warnings_embed.set_footer(text=f"Embed created from {self.bot.user}")
                await ctx.respond(embed=warnings_embed, ephemeral=True)
            else:
                no_warnings_embed = discord.Embed(
                    color=discord.Color.green(),
                    description=f"{member.mention} has no warnings.")
                no_warnings_embed.set_thumbnail(url=member.display_avatar)
                no_warnings_embed.set_footer(text=f"Embed created from {self.bot.user}")
                await ctx.respond(embed=no_warnings_embed,ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    @slash_command(description='remove warn from a specific user')
    @commands.has_permissions(ban_members=True)
    async def removewarn(self, ctx, member: discord.Member):
        try:
            self.remove_last_warning(ctx.guild.id, member.id)
            remove_warn_embed = discord.Embed(
                color=discord.Color.green(),
                description=f"The last warning for {member.mention} has been removed."
            )
            remove_warn_embed.set_thumbnail(url=member.display_avatar)
            remove_warn_embed.set_footer(text=f"Embed created from {self.bot.user}")
            await ctx.respond(embed=remove_warn_embed,ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    def cog_unload(self):
        self.conn.close()

def setup(bot):
    bot.add_cog(WarnSystem(bot))
