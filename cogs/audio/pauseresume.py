from datetime import datetime
import discord
import wavelink
from discord.ext import commands

class PauseResume(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="pause", with_app_command=True)
    async def pause(self, ctx: commands.Context):
        """Pause the bot.

        The user must be connected to the voice channel that the bot is playing in.
        """
        author = ctx.message.author
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("I am not currently connected to a voice channel.")

        if author not in vc.channel.members:
            return await ctx.send("You must be in the same voice channel as me to use this command.")
        
        if not vc.is_playing():
            return await ctx.send("I am not currently playing.")

        await vc.pause()
        await ctx.send("Pausing track.")
    
    @commands.hybrid_command(name="resume", with_app_command=True)
    async def resume(self, ctx: commands.Context):
        """Resume the bot.

        The user must be connected to the voice channel that the bot is playing in.
        """
        author = ctx.message.author
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("I am not currently connected to a voice channel.")

        if author not in vc.channel.members:
            return await ctx.send("You must be in the same voice channel as me to use this command.")
        
        if not vc.is_paused():
            return await ctx.send("I am not currently playing or paused.")

        await vc.resume()
        await ctx.send("Resuming track.")
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PauseResume(bot))
