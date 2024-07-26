import json
import os
import sys

import discord
from bot.cogs.autoroles import Autoroles, Verification
from discord.ext import commands

data_path = f"{os.getcwd()}/bot/data/data.json"
with open(data_path, encoding="utf-8") as file:
    data = json.load(file)

if not os.path.isfile(data["ConfigPath"]):
    sys.exit(
        "¡No existe el archivo 'config.json', por favor añadelo y vuelve a ejecutar el bot!"
    )
else:
    with open(data["ConfigPath"]) as file:
        config = json.load(file)
TOKEN = config["token"]

WordsStructure = {"banned_words": []}
LinksStructure = {"bad_domains": []}

for files in data["DataPaths"].values():
    if not os.path.exists(files):
        if files.endswith("words.json"):
            with open(files, "w") as file:
                json.dump(WordsStructure, file)
        elif files.endswith("links.json"):
            with open(files, "w") as file:
                json.dump(LinksStructure, file)
        elif files.endswith("tags.json"):
            with open(files, "w") as file:
                json.dump({}, file)
        else:
            print(f"Hubo un error al crear el archivo {files}.")

    with open(files, encoding="utf-8") as file:
        if files.endswith("words.json"):
            words = json.load(file)
        elif files.endswith("links.json"):
            links = json.load(file)
        elif files.endswith("tags.json"):
            tags = json.load(file)
        else:
            print(f"Hubo un error al cargar el archivo {files}.")


class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=discord.Intents().all(),
            help_command=None,
        )

        self.cogs_loaded = []

    async def setup_hook(self) -> None:
        for root, d, files in os.walk(f"{os.getcwd()}/bot/cogs", topdown=True):
            for f in files:
                if f.endswith(".py"):
                    dir = root[len(f"{os.getcwd()}/bot/cogs/") :]
                    dir = dir.replace(os.sep, ".")
                    cog = f[:-3]
                    await self.load_extension(
                        f"cogs.{dir}.{cog}" if dir else f"cogs.{cog}"
                    )
                    self.cogs_loaded.append(f"{cog}")

        client.add_view(Verification())
        client.add_view(Autoroles())


client = Client()


client.config = config
client.data = data
client.words = words
client.links = links

client.run(TOKEN)
