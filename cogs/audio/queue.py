from datetime import datetime
import asyncio
import discord
import wavelink
from discord.ext import commands
        
class Queue(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.timer = None
        self.loop_queue = False
        
    async def disconnect_timer(self):
        await asyncio.sleep(7200)  # aspetta 2 ore (7200 secondi)
        await self.vc.stop()
        await self.bot.disconnect()  # disconnetti il bot

    @commands.hybrid_command(name="queue", with_app_command=True)
    async def queue_command(self, ctx: commands.Context) -> None:
        """Show queued songs.

        Args:
            ctx (commands.Context): _description_
        """

        if not ctx.author.voice:
            await ctx.send("You are not connected to any voice channel.")
            return

        vc: wavelink.Player = ctx.voice_client

        if vc is None:
            await ctx.send("Bot is not playing anything.")
            return

        if not vc.queue.is_empty:
            await ctx.send(embed=self.get_queue_embed(ctx))
        else:
            await ctx.send("Queue is empty.")
            
#clearqueue

    @commands.hybrid_command(name="clearqueue", with_app_command=True)
    async def clearqueue_command(self, ctx: commands.Context) -> None:
        """Clear the queued songs.
        
        Args:
            ctx (commands.Context): _description_
        """
        
        if not ctx.author.voice:
            await ctx.send("You are not connected to any voice channel.")
            return

        vc: wavelink.Player = ctx.voice_client

        if vc is None:
            await ctx.send("Bot is not playing anything.")
            return
        if vc.queue.is_empty:
            await ctx.send("Queue is already empty.")
            return
        try:
            vc.queue.clear()
            await ctx.send("Queue cleared.")
        except Exception as e:
            logger.exception(f"Error clearing queue: {e}")

#loopenable

    @commands.hybrid_command(name="loop", with_app_command=True)
    async def loop_command(self, ctx: commands.Context) -> None:
        """Enable/Disable the loop for the queue (2h max).

        Args:
            ctx (commands.Context): _description_
        """
        try:
            if not ctx.author.voice:
               await ctx.send("You are not connected to any voice channel.")
               return

            vc: wavelink.Player = ctx.voice_client

            if vc is None:
               await ctx.send("Bot is not playing anything.")
               return

            if vc.queue.is_empty:
               await ctx.send("Queue is empty, cannot start loop.")
               return

            self.loop_queue = not self.loop_queue
            if self.loop_queue:
               await ctx.send("Queue loop is now enabled.")
               self.timer = self.bot.loop.create_task(self.disconnect_timer())
            else:
               await ctx.send("Queue loop is now disabled.")
               if self.timer:
                  self.timer.cancel()
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            
#playing

    @commands.hybrid_command(name="playing", with_app_command=True)
    async def playing_command(self, ctx: commands.Context) -> None:
        """Show currently playing song.

        Args:
            ctx (commands.Context): _description_
        """

        if not ctx.author.voice:
            await ctx.send("You are not connected to any voice channel.")
            return

        vc: wavelink.Player = ctx.voice_client

        if vc is None:
            await ctx.send("Bot is not playing anything.")
            return

        if not vc.is_playing or not vc.track:
            await ctx.send("Bot is not playing anything.")
        else:
            await ctx.send(embed=self.get_playing_embed(ctx))

#fine comandi

    def get_queue_embed(self, ctx: commands.Context) -> discord.Embed:
        """_summary_

        Args:
            ctx (commands.Context): _description_

        Returns:
            discord.Embed: _description_
        """
        vc: wavelink.Player = ctx.voice_client

        embed = discord.Embed(
            title="Queue",
            description=f"Showing up to next {10} tracks",
            colour=ctx.author.colour,
            timestamp=datetime.utcnow(),
        )

        embed.set_author(name="Query Results")

        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        if vc.track:
            embed.add_field(
                name="Currently playing",
                value=vc.track.title[0:1023],
                inline=False,
            )

        value = ""
        for track in vc.queue:
            value += f"\n {track.title}"

        embed.add_field(
            name="Next up",
            value=value[0:1023],
            inline=False,
        )

        return embed

    def get_playing_embed(self, ctx: commands.Context) -> discord.Embed:
        """Display info of currently playing audio.

        Args:
            ctx (commands.Context): _description_

        Returns:
            discord.Embed: _description_
        """

        vc: wavelink.Player = ctx.voice_client

        embed = discord.Embed(
            title="Now playing",
            colour=ctx.author.colour,
            timestamp=datetime.utcnow(),
        )
        embed.set_author(name="Playback Information")
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        embed.add_field(name="Track title", value=vc.track.title, inline=False)
        embed.add_field(
            name="Artist",
            value=vc.track.author if vc.track.author else "None",
            inline=False,
        )
        embed.add_field(
            name="URI", value=vc.track.uri if vc.track.uri else "None", inline=False
        )

        if isinstance(vc.track, wavelink.YouTubeTrack):
            embed.set_image(url=vc.track.thumbnail)

        position = divmod(vc.position, 60000)
        length = divmod(vc.track.length, 60000)
        embed.add_field(
            name="Position",
            value=f"{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}",
            inline=False,
        )

        return embed


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Queue(bot))
