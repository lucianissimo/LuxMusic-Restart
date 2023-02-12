from datetime import datetime

import discord
import wavelink
from discord import app_commands
from discord.ext import commands


class Stop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="stop", with_app_command=True)
    async def stop_command(self, ctx: commands.Context):
        """Stops the bot.

        The user must be connected to the voice channel that the bot is playing in.
        """

        if not ctx.author.voice:
            await ctx.send("You are not connected to any voice channel.")
            return

        if ctx.voice_client.channel is None:
            await ctx.send("Bot is not playing anything.")
            return

        if ctx.voice_client.channel.id != ctx.author.voice.channel.id:
            await ctx.send(
                "Join the voice channel the bot is playing in to disconnect it."
            )
            return

        await self.stop_player(ctx.guild)
        await ctx.send(
            f"Stopped by {ctx.author.mention} on {discord.utils.format_dt(datetime.now())} ."
        )

    async def stop_player(self, guild: discord.Guild):
        """Stops the player and disconnects the bot from the voice channel.

        Args:
            guild (discord.Guild): The guild the player is playing in.
        """
        player = self.bot.wavelink_node.get_player(guild)

        # need to check this because this will be fired two times
        # if disconnected using commands
        if player is not None:
            await player.stop()
            player.queue.clear()
            await player.disconnect()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Stop(bot))