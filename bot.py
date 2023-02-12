import asyncio
import logging
import discord

from core.bot import Bot
from cogs.audio import context_menu_commands

# bot intents

bot = Bot(intents=discord.Intents.all())

logger = logging.getLogger(__name__)

# inizio codice timer left channel dopo 15 minuti

async def disconnect_task(voice_client, after):
    await asyncio.sleep(900)  # 15 minutes
    if len(after.channel.members) == 1:
        try:
            await voice_client.disconnect()
        except Exception as e:
            logger.exception(f"Error disconnecting from voice channel: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
    if not after.channel:
        return

    if len(after.channel.members) == 1:
        voice_client = discord.utils.get(client.voice_clients, guild=after.guild)
        if voice_client and voice_client.is_connected() and voice_client.channel == after.channel:
            try:
                asyncio.create_task(disconnect_task(voice_client, after))
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
