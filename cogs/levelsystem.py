import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.utils import get
import sqlite3
import os
import logging


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB_path = os.path.abspath("C:/Users/Olive/Documents/DiscordBot/databases")
        db_file = os.path.join(self.DB_path, 'Levelsystem.db')
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                xp INTEGER,
                level INTEGER
            )
        ''')
        self.conn.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Cog {self.__class__.__name__} is ready.')

    def create_default_role(self, guild, role_name):
        permissions = discord.Permissions(send_messages=True, read_messages=True)
        return guild.create_role(name=role_name, permissions=permissions)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Add XP to the user
        self.add_xp(message.guild.id, message.author.id, 10)

        # Check if the user leveled up
        if self.check_level_up(message.guild.id, message.author.id):
            await self.check_and_assign_role(message.guild, message.author)

    def add_xp(self, guild_id, user_id, xp):
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (guild_id, user_id, xp, level)
            VALUES (?, ?, 0, 1)
        ''', (guild_id, user_id))

        self.cursor.execute('''
            UPDATE users SET xp = xp + ? WHERE guild_id = ? AND user_id = ?
        ''', (xp, guild_id, user_id))

        self.conn.commit()

    def check_level_up(self, guild_id, user_id):
        self.cursor.execute('''
            SELECT xp, level FROM users WHERE guild_id = ? AND user_id = ?
        ''', (guild_id, user_id))

        xp, level = self.cursor.fetchone()

        if xp >= level * 100:
            self.cursor.execute('''
                UPDATE users SET xp = 0, level = level + 1
                WHERE guild_id = ? AND user_id = ?
            ''', (guild_id, user_id))
            self.conn.commit()
            return True

        return False

    async def check_and_assign_role(self, guild, user):
        level = self.get_level(guild.id, user.id)
        role_name = f'Level {level} Role'

        # Check if the role exists, otherwise create it
        role = get(guild.roles, name=role_name)
        if not role:
            role = await self.create_default_role(guild, role_name)

        # Add the role to the user
        await user.add_roles(role)

    def get_level(self, guild_id, user_id):
        self.cursor.execute('''
            SELECT level FROM users WHERE guild_id = ? AND user_id = ?
        ''', (guild_id, user_id))

        result = self.cursor.fetchone()
        return result[0] if result else 1

    @slash_command(description="shows your rank")
    async def rank(self, ctx, member: discord.Member = None):
        try:
            member = member or ctx.author

            level = self.get_level(ctx.guild.id, member.id)
            xp = self.get_xp(ctx.guild.id, member.id)

            embed = discord.Embed(
                title=f'{member.display_name}\'s Rank',
                color=discord.Color.blue()
            )
            embed.add_field(name='Level', value=level, inline=True)
            embed.add_field(name='XP', value=xp, inline=True)
            embed.set_thumbnail(url=member.display_avatar)

            await ctx.respond(embed=embed, ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    @slash_command(description="shows the leaderboard")
    async def leaderboard(self, ctx):
        try:
            self.cursor.execute('''
                SELECT user_id, level FROM users WHERE guild_id = ? ORDER BY level DESC
            ''', (ctx.guild.id,))

            rows = self.cursor.fetchmany(10)  # Get top 10 users
            leaderboard_embed = discord.Embed(
                title=f'{ctx.guild.name} Leaderboard',
                color=discord.Color.gold()
            )

            for rank, row in enumerate(rows, start=1):
                user_id, level = row
                member = ctx.guild.get_member(user_id)
                leaderboard_embed.add_field(
                    name=f'{rank}. {member.display_name}' if member else f'{rank}. User Left',
                    value=f'Level {level}',
                    inline=False
                )
                leaderboard_embed.set_thumbnail(url=member.display_avatar)

            await ctx.respond(embed=leaderboard_embed, ephemeral=True)
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)

    def get_xp(self, guild_id, user_id):
        self.cursor.execute('''
            SELECT xp FROM users WHERE guild_id = ? AND user_id = ?
        ''', (guild_id, user_id))

        result = self.cursor.fetchone()
        return result[0] if result else 0

def setup(bot):
    bot.add_cog(LevelSystem(bot))
