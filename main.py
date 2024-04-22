import json
import os
import sys

import discord
from discord.ext import commands

from cogs.core.autoroles import Autoroles, Verification

data_path = f"{os.getcwd()}/data/data.json"
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

        self.dirs = [
            f"{os.getcwd()}/cogs/cmds",
            f"{os.getcwd()}/cogs/core",
        ]
        self.cogs_loaded = []

    async def setup_hook(self) -> None:
        for dir in self.dirs:
            for file in os.listdir(dir):
                if file.endswith(".py"):
                    cog = file[:-3]
                    if dir.endswith("cmds"):
                        await self.load_extension(f"cogs.cmds.{cog}")
                        self.cogs_loaded.append(f"cmds.{cog}")
                    elif dir.endswith("core"):
                        await self.load_extension(f"cogs.core.{cog}")
                        self.cogs_loaded.append(f"core.{cog}")
                    else:
                        print(f"Ha ocurrido un error cargando el cog {cog}.")
        client.add_view(Verification())
        client.add_view(Autoroles())


client = Client()


client.config = config
client.data = data
client.words = words
client.links = links

client.run(TOKEN)
