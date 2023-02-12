import os
import platform
import asyncio
import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """_summary_"""

        print(f"Loggato come {self.bot.user.name}")
        print(f"Discord.py Versione API: {discord.__version__}")
        print(f"Versione Python: {platform.python_version()}")
        print(f"Avviato su: {platform.system()} {platform.release()} ({os.name})")
        print("-------------------")

        await self.bot.change_presence(
            activity=discord.Streaming(
                name="Use slash commands.",
                url="https://www.twitch.tv/pewdiepie",
                platform="Twitch",
                twitch_name="pewdiepie",
            )
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
