import discord
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()

intents = discord.Intents.all()
debug_guilds_env = os.environ.get('DEBUG_GUILDS', '')
bot = discord.Bot(
    intents=intents,
    debug_guilds=[int(guild_id) for guild_id in debug_guilds_env.split(',') if guild_id]# Guild id's
)

log_formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = RotatingFileHandler('bot.log', maxBytes=5 * 1024 * 1024, backupCount=2)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(file_handler)


@bot.event
async def on_ready():
    print(f"{bot.user} ist online")
    logging.info(f'Logged in as {bot.user.name} ({bot.user.id})')


if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv("TOKEN"))
