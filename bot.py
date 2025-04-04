import asyncio
import os
import sys
import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# Create a logger
LOG = logging.getLogger('discord')
LOG.setLevel(logging.DEBUG)

# Create a rotating file handler
file_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)  

# Create a stream handler for logging to the console
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.INFO) 

# Format logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
LOG.addHandler(stream_handler)
LOG.addHandler(file_handler)
LOG.info("logger online")

description = 'Halvor Persson (born 11 March 1966) is a Norwegian former ski jumper.'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='>', description=description, intents=intents)

async def load_cogs():
    await bot.load_extension("cogs.commands")
    await bot.load_extension("cogs.wikigame")

@bot.event
async def on_ready():
    LOG.info(f'{bot.user} has connected to Discord!')
    
async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv('BOT_TOKEN'))

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())

    