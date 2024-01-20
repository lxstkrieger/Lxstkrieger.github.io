import discord
from discord.ext import commands
from discord.commands import slash_command
from youtubesearchpython import VideosSearch
import yt_dlp
import asyncio
import subprocess

voice_clients = {}
ffmpeg_options = {'options': '-vn -bufsize 64k', 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}

class Music(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.queue = {}

    async def play_next(self, ctx):
        if ctx.guild.id in self.queue and self.queue[ctx.guild.id]:
            next_song = self.queue[ctx.guild.id].pop(0)
            await self.play(ctx, next_song)
        else:
            voice_client = voice_clients.get(ctx.guild.id)
            if voice_client and voice_client.is_connected():
                if not voice_client.is_playing():
                    await voice_client.disconnect()

    async def play(self, ctx, song):
        try:
            if ctx.guild.id not in voice_clients or not voice_clients[ctx.guild.id].is_connected():
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            else:
                voice_client = voice_clients[ctx.guild.id]

            ydl_opts = {
                'format': 'bestaudio',
                'extract_flat': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'opus',
                    'preferredquality': '192',
                }],
                'outtmpl': 'temp_audio.%(ext)s',
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song['url'], download=False)

            audio_url = info['url']
            player = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options, stderr=subprocess.DEVNULL)

            def after_playing(error):
                asyncio.ensure_future(self.play_next(ctx))

            voice_client.play(player, after=after_playing)
        except Exception as err:
            print(err)

    @slash_command()
    async def play(self, ctx, query: str):
        try:
            await ctx.defer()
            video_search = VideosSearch(query, limit=1)
            video_info = video_search.result()['result'][0]
            video_url = video_info['link']

            song = {'title': video_info['title'], 'url': video_url}

            if ctx.guild.id not in self.queue:
                self.queue[ctx.guild.id] = [song]
                await self.play(ctx, song)

                embed = discord.Embed(
                    title="Now playing",
                    description=f"**{song['title']}**",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=ctx.guild.icon)
                await ctx.respond(embed=embed)
            else:
                self.queue[ctx.guild.id].append(song)
        except Exception as err:
            print(err)

    @slash_command()
    async def skip(self, ctx):
        try:
            voice_client = voice_clients.get(ctx.guild.id)
            if voice_client and voice_client.is_playing():
                voice_client.stop()
                await self.play_next(ctx)
                await ctx.respond("Song skipped.")
            else:
                await ctx.respond("There is no song to skip.")
        except Exception as err:
            print(err)

    @slash_command()
    async def pause(self, ctx):
        try:
            voice_clients[ctx.guild.id].pause()
            pause_embed = discord.Embed(
                title="Song was paused!",
                color=discord.Color.magenta(),
            )
            await ctx.respond(embed=pause_embed, ephemeral=True)
        except Exception as err:
            print(err)

    @slash_command()
    async def resume(self, ctx):
        try:
            voice_clients[ctx.guild.id].resume()
            resume_embed = discord.Embed(
                title="Song was resumed!",
                color=discord.Color.magenta(),
            )
            await ctx.respond(embed=resume_embed, ephemeral=True)
        except Exception as err:
            print(err)

    @slash_command()
    async def stop(self, ctx):
        try:
            if ctx.guild.id in self.queue:
                del self.queue[ctx.guild.id]
            voice_clients[ctx.guild.id].stop()

            stop_embed = discord.Embed(
                title="Song was stopped!",
                color=discord.Color.magenta(),
            )
            await ctx.respond(embed=stop_embed, ephemeral=True)
        except Exception as err:
            print(err)

    @slash_command()
    async def queue(self, ctx):
        try:
            await ctx.defer()
            if ctx.guild.id in self.queue and self.queue[ctx.guild.id]:
                queue_list = "\n".join([f"{i + 1}. {song['title']} by {song.get('artist', 'Unknown')}" for i, song in enumerate(self.queue[ctx.guild.id])])
                embed = discord.Embed(
                    title="Queue",
                    description=queue_list,
                    color=discord.Color.blue()
                )
                await ctx.respond(embed=embed)
            else:
                no_queue_embed = discord.Embed(
                    title="The queue is empty.",
                    color=discord.Color.blurple()
                )
                await ctx.respond(embed=no_queue_embed)
        except Exception as err:
            print(err)


def setup(bot: discord.Bot):
    bot.add_cog(Music(bot))
