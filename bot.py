import asyncio
import logging
import discord

from typing import Optional
from core.bot import Bot
from cogs.audio import context_menu_commands

# bot intents

bot = Bot(intents=discord.Intents.all())

logger = logging.getLogger(__name__)

# inizio codice timer left channel dopo 15 minuti

async def disconnect_task(bot, voice_client, after):
    try:
        await asyncio.sleep(900)  # 15 minutes
        while len(after.channel.members) == 1:
            await voice_client.disconnect()
    except Exception as e:
        logger.exception(f"Error disconnecting from voice channel: {e}")
    else:
        logger.info("Bot has disconnected from voice channel due to inactivity.")
        
@bot.event
async def on_voice_state_update(member, before, after):
    if not after.channel:
        return

    if len(after.channel.members) == 1:
        voice_client = discord.utils.get(bot.voice_clients, guild=after.guild)
        if voice_client and voice_client.is_connected() and voice_client.channel == after.channel:
            try:
                asyncio.create_task(disconnect_task(bot, voice_client, after))
            except Exception as e:
                logger.exception(f"Error creating disconnect task: {e}")

# fine timer

async def main():
    await bot.load_extension("cogs.audio.disconnect")
    await bot.load_extension("cogs.audio.listeners")
    await bot.load_extension("cogs.audio.play")
    await bot.load_extension("cogs.audio.skip")
    await bot.load_extension("cogs.audio.queue")
    await bot.load_extension("cogs.audio.stop")
    await bot.load_extension("cogs.audio.pauseresume")
    await bot.load_extension("cogs.events")
    
    
    context_menu_commands.init(bot)
 
asyncio.run(main())

bot.run(bot.config["token"])
