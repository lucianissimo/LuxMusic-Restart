import asyncio
import logging
import discord
import wavelink
from discord.ext import commands
from typing import Optional
from core.bot import Bot
from cogs.audio import context_menu_commands
from cogs import error_handler

# bot intents

bot = Bot(intents=discord.Intents.all())

logger = logging.getLogger(__name__)

# inizio codice timer left channel dopo 15 minuti

@bot.event
async def disconnect_task(bot, voice_client, after):
    try:
        await asyncio.sleep(900)  # 15 minutes
        while len(after.channel.members) == 1:
            await voice_client.disconnect()
    except Exception as e:
        logger.exception(f"Error disconnecting from voice channel: {e}")
    else:
        logger.info("Bot has disconnected from voice channel due to inactivity.")
        
# fine

async def main():
    await bot.load_extension("cogs.error_handler")
    await bot.load_extension("cogs.audio.disconnect")
    await bot.load_extension("cogs.audio.listeners")
    await bot.load_extension("cogs.audio.play")
    await bot.load_extension("cogs.audio.skip")
    await bot.load_extension("cogs.audio.queue")
    await bot.load_extension("cogs.audio.stop")
    await bot.load_extension("cogs.audio.pauseresume")
    await bot.load_extension("cogs.events")
    context_menu_commands.init(bot)
    


try:
    asyncio.run(main())
except Exception as e:
    print(f"Error running bot: {e}")

bot.run(bot.config["token"])
