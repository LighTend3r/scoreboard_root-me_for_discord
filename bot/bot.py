import discord
import asyncio
import os
from discord.ext import commands
from utils.config import DISCORD_TOKEN
from utils.db import init_db
import logging as log
from utils.logging import info



l_handler = log.StreamHandler()
l_formatter = log.Formatter(
    "%(asctime)s [%(levelname)s] (discord): %(message)s",
    datefmt="[%m/%d/%Y %I:%M:%S %p]",
)

discord.utils.setup_logging(
    level=log.INFO, handler=l_handler, formatter=l_formatter, root=False
)

intents = discord.Intents.all()
intents.members = True

init_db()




async def main():
    async with bot:

        bot.remove_command("help")


        file_path = os.path.abspath(os.path.dirname(__file__))

        for f in os.listdir(f"{file_path}/commands"):
            if f.endswith(".py"):
                await bot.load_extension("commands." + f[:-3])
                info(f"Command {f} loaded")


        for f in os.listdir(f"{file_path}/events"):
            if f.endswith(".py"):
                await bot.load_extension("events." + f[:-3])
                info(f"Event {f} loaded")

        for f in os.listdir(f"{file_path}/tasks"):
            if f.endswith(".py"):
                await bot.load_extension("tasks." + f[:-3])
                info(f"Task {f} loaded")

        await bot.start(DISCORD_TOKEN)


bot = commands.Bot(command_prefix='!', intents=intents)

asyncio.run(main())
