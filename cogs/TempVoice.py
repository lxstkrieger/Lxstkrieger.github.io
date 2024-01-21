import discord
from discord.ext import commands
from discord.commands import slash_command
import logging


class TemporaryVoice(commands.Cog):
    temporary_channels = {}
    temporary_categories = {}
    locked_channels = set()

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        possible_channel_name = f"{member.display_name}'s area"

        if after.channel:
            if after.channel.name == "temp":
                temp_channel = await after.channel.clone(name=possible_channel_name)
                self.temporary_channels[member.id] = temp_channel.id
                await member.move_to(temp_channel)
            elif after.channel.name == 'teams':
                temporary_category = await after.channel.guild.create_category(name=possible_channel_name)
                await temporary_category.create_text_channel(name="text")
                temp_channel = await temporary_category.create_voice_channel(name="voice")
                self.temporary_categories[member.id] = temporary_category.id
                await member.move_to(temp_channel)

        if before.channel:
            if member.id in self.temporary_channels and before.channel.id == self.temporary_channels[member.id]:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    del self.temporary_channels[member.id]

            if member.id in self.temporary_categories and before.channel.category.id == self.temporary_categories[
                member.id]:
                if len(before.channel.members) == 0:
                    for channel in before.channel.category.channels:
                        await channel.delete()
                    await before.channel.category.delete()
                    del self.temporary_categories[member.id]

    @slash_command(name='lock')
    async def lock_channel(self, ctx):
        try:
            member_id = ctx.author.id
            if member_id in self.temporary_channels and ctx.author.voice.channel.id == self.temporary_channels[
                member_id]:
                voice_channel = self.bot.get_channel(self.temporary_channels[member_id])
                if voice_channel.created_at and voice_channel.created_at == ctx.author.joined_at:
                    self.locked_channels.add(voice_channel.id)
                    await ctx.send(f"{ctx.author.mention}, the channel has been locked. No one can join anymore.")
                else:
                    await ctx.send("You can only lock temporary channels that you have created.")
            else:
                await ctx.send("You can only lock the temporary channel you have created.")
        except Exception as e:
            logging.error(f'An error occurred in {self.__class__.__name__}: {e}', exc_info=True)


def setup(bot: discord.Bot):
    bot.add_cog(TemporaryVoice(bot))
