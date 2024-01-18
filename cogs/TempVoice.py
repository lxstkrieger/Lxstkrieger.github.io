import discord
from discord.ext import commands
from discord.commands import slash_command
import logging


class TemporaryVoice(commands.Cog):

    temporary_channels = []
    temporary_categories = []

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        possible_channel_name = f"{member.display_name}'s area"
        if after.channel:
            if after.channel.name == "temp":
                temp_channel = await after.channel.clone(name=possible_channel_name)
                await member.move_to(temp_channel)
                self.temporary_channels.append(temp_channel.id)
            if after.channel.name == 'teams':
                temporary_category = await after.channel.guild.create_category(name=possible_channel_name)
                await temporary_category.create_text_channel(name="text")
                temp_channel = await temporary_category.create_voice_channel(name="voice")
                await member.move_to(temp_channel)
                self.temporary_categories.append(temp_channel.id)

        if before.channel:
            if before.channel.id in self.temporary_channels:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
            if before.channel.id in self.temporary_categories:
                if len(before.channel.members) == 0:
                    for channel in before.channel.category.channels:
                        await channel.delete()
                    await before.channel.category.delete()

    @slash_command(name='lock')
    async def lock_channel(self, ctx):
        try:
            voice_channel = ctx.author.voice.channel

            if voice_channel:
                if voice_channel.id in self.temporary_channels and voice_channel.id not in self.locked_channels:
                    if voice_channel.created_at and voice_channel.created_at == ctx.author.joined_at:
                        self.locked_channels.add(voice_channel.id)
                        await ctx.send(f"{ctx.author.mention}, the channel has been blocked. No one can join anymore. ")
                    else:
                        await ctx.send("You can only block temporary channels that you have created.")
                else:
                    await ctx.send("You can only block temporary channels that you have already joined.")
            else:
                await ctx.send("You must be in a voice channel to use this command.")
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(TemporaryVoice(bot))
