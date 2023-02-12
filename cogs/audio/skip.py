import wavelink
from discord.ext import commands

class Skip(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="skip", with_app_command=True)
    async def skip_command(self, ctx: commands.Context):
        """Skips currently playing song and play next song in queue.

        Args:
            ctx (commands.Context): The context passed in by the command.
        """
        # Check if the author is connected to a voice channel
        if not ctx.author.voice:
            await ctx.send("You are not connected to any voice channel.")
            return

        vc: wavelink.Player = ctx.voice_client

        # Check if the bot is not playing anything
        if vc is None:
            await ctx.send("Bot is not playing anything.")
            return
        
        # Check if the author is in the same voice channel as the bot
        if vc.channel.id != ctx.author.voice.channel.id:
            await ctx.send("Join the voice channel the bot is playing in to use the `skip` command.")
            return

        # Check if there is anything in the queue to skip
        if not vc.queue.is_empty:
            await vc.stop()
            await ctx.send(f"Now playing: {vc.queue[0].title}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Skip(bot))
