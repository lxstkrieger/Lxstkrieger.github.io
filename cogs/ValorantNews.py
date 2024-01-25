import discord
from discord.ext import commands
from discord.commands import slash_command
import logging


class ValorantNews(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    API_URL = 'https://vlrggapi.vercel.app/news'


    async def get_latest_news():
        try:
            response = requests.get(API_URL)
            data = response.json()
            return data["data"]["segments"]
        except Exception as e:
            print(f"Fehler beim Abrufen der News: {e}")
            return None

    async def send_news_to_channel(news, channel_name):
        if news:
            channel = discord.utils.get(client.guilds[0].channels, name=channel_name)

            if channel:
                for segment in news:
                    embed = discord.Embed(
                        title=segment["title"],
                        description=segment["description"],
                        color=discord.Color.green()
                    )
                    embed.set_author(name=segment["author"])
                    embed.add_field(name="Datum", value=segment["date"], inline=False)
                    embed.add_field(name="URL", value=f"[Mehr erfahren]({segment['url_path']})", inline=False)

                    await channel.send(embed=embed)
            else:
                print(f"Kanal '{channel_name}' nicht gefunden.")

    @commands.Cog.listener()
    async def on_ready():
        print(f'Eingeloggt als {self.bot.user.name} ({self.bot.user.id})')
        news_check.start()

    @tasks.loop(minutes=30)
    async def news_check():
        latest_news = await get_latest_news()

        # Hier kannst du die Kanalnamen anpassen und weitere hinzufügen
        for channel_name in ["valorant-news"]:
            await send_news_to_channel(latest_news, channel_name)


def setup(bot: discord.Bot):
    bot.add_cog(ValorantNews(bot))
