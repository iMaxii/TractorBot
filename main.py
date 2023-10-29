import asyncio
import json
import os
import sys

import aiosqlite
import discord
from discord.ext import commands

# Load json files
config_path = f"{os.path.realpath(os.path.dirname(__file__))}/config.json"
data_path = f"{os.path.realpath(os.path.dirname(__file__))}/data/data.json"
banned_words_path = (
    f"{os.path.realpath(os.path.dirname(__file__))}/data/banned_words.json"
)
banned_links_path = (
    f"{os.path.realpath(os.path.dirname(__file__))}/data/banned_links.json"
)
if not os.path.isfile(config_path):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(config_path) as file:
        config = json.load(file)
TOKEN = config["token"]

with open(data_path, encoding="utf-8") as file:
    data = json.load(file)

with open(banned_words_path, encoding="utf-8") as file:
    words = json.load(file)

with open(banned_links_path, encoding="utf-8") as file:
    links = json.load(file)


class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=discord.Intents().all(),
            help_command=None,
        )

        self.cogslist = [
            "cogs.commands.util",
            "cogs.commands.fun",
            "cogs.commands.help",
            "cogs.commands.owner",
            "cogs.commands.tag",
            "cogs.commands.mod",
            "cogs.core.automod",
            "cogs.core.events",
            "cogs.core.errors",
            "cogs.core.autoroles",
        ]

    async def setup_hook(self):
        for cog in self.cogslist:
            await self.load_extension(cog)


client = Client()


async def init_db():
    async with aiosqlite.connect(
        f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db"
    ) as db:
        with open(
            f"{os.path.realpath(os.path.dirname(__file__))}/database/schema.sql"
        ) as file:
            await db.executescript(file.read())
        await db.commit()


client.config = config
client.data = data
client.words = words
client.links = links

asyncio.run(init_db())
client.run(TOKEN)
