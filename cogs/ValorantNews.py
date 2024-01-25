import discord
from discord.ext import commands, tasks
import requests


class ValorantNews(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.API_URL = 'https://vlrggapi.vercel.app/news'

    async def get_latest_news(self):
        try:
            response = requests.get(self.API_URL)
            data = response.json()
            return data["data"]["segments"][0]
        except Exception as e:
            print(f"Fehler beim Abrufen der News: {e}")
            return None

    async def send_news_to_channel(self, news, channel_name):
        if news:
            channel = discord.utils.get(self.bot.guilds.channels, name=channel_name)

            if channel:
                embed = discord.Embed(
                    title=news["title"],
                    description=news["description"],
                    color=discord.Color.magenta()
                )
                embed.set_author(name=news["author"])
                embed.add_field(name="Datum", value=news["date"], inline=False)
                embed.add_field(name="URL", value=f"[Mehr erfahren]({news['url_path']})", inline=False)

                await channel.send(embed=embed)
            else:
                print(f"Kanal '{channel_name}' nicht gefunden.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Eingeloggt als {self.bot.user.name} ({self.bot.user.id})')
        self.news_check.start()

    @tasks.loop(minutes=30)
    async def news_check(self):
        latest_news = await self.get_latest_news()
        for channel_name in ["valorant-news"]:
            await self.send_news_to_channel(latest_news, channel_name)


def setup(bot: discord.Bot):
    bot.add_cog(ValorantNews(bot))
