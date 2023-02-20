from datetime import datetime, timedelta
import discord
import wavelink
import asyncio
from discord.ext import commands

class PauseResume(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.is_paused = False
        self.pause_start = None
        self.pause_task = None

    @commands.hybrid_command(name="pause", with_app_command=True)
    async def pause(self, ctx: commands.Context):
        """Pause the bot.

        The user must be connected to the voice channel that the bot is playing in.
        """
        author = ctx.message.author
        vc = ctx.voice_client

        try:
            if not vc or not vc.is_connected():
                return await ctx.send("I am not currently connected to a voice channel.")

            if author not in vc.channel.members:
                return await ctx.send("You must be in the same voice channel as me to use this command.")

            if not vc.is_playing():
                return await ctx.send("I am not currently playing.")

            self.is_paused = True
            self.pause_start = datetime.utcnow()
            await vc.pause()
            await ctx.send("Pausing track.")
            if not self.pause_task:  # start the task loop only if it's not already running
                self.pause_task = self.bot.loop.create_task(self.check_pause(vc.channel, vc))

        except Exception as e:
            await ctx.send(f"An error occurred while trying to pause the bot: {e}")

    @commands.hybrid_command(name="resume", with_app_command=True)
    async def resume(self, ctx: commands.Context):
        """Resume the bot.

        The user must be connected to the voice channel that the bot is playing in.
        """
        author = ctx.message.author
        vc = ctx.voice_client

        try:
            if not vc or not vc.is_connected():
                return await ctx.send("I am not currently connected to a voice channel.")

            if author not in vc.channel.members:
                return await ctx.send("You must be in the same voice channel as me to use this command.")

            if not vc.is_paused():
                return await ctx.send("I am not currently playing or paused.")

            self.is_paused = False
            self.pause_start = None
            await vc.resume()
            await ctx.send("Resuming track.")
            if self.pause_task:  # cancel the task loop if it's running
                self.pause_task.cancel()
                self.pause_task = None

        except Exception as e:
            await ctx.send(f"An error occurred while trying to resume the bot: {e}")

    async def check_pause(self, channel, vc):
        """Check if the bot is paused for more than 30 minutes and disconnect if it is."""
        try:
            while True:
                if self.is_paused:
                    if datetime.utcnow() - self.pause_start > timedelta(minutes=30):
                        await channel.send("I've been paused for too long, disconnecting now.")
                        await vc.disconnect()
                        break
                else:  # the bot is not paused anymore, stop the task loop
                    break
                await asyncio.sleep(60)  # wait 1 minute before checking again

        except Exception as e:
            await channel.send(f"An error occurred while trying to check if the bot has been paused for too long: {e}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PauseResume(bot))
