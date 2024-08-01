import os
import platform
import random

import discord
from discord.ext import commands, tasks


class EventsCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"""
===============================================
        __                  __
       / /__________ ______/ /_____  _____
      / __/ ___/ __ `/ ___/ __/ __ \/ ___/
     / /_/ /  / /_/ / /__/ /_/ /_/ / /
     \__/_/   \__,_/\___/\__/\____/_/

===============================================

###############################################
#            Bot creado por iMaxii            #
#          https://github.com/iMaxii          # 
#                                             #
#     Unete al Discord de la Tractor Army     #
#         https://discord.gg/74SJhxT6Nt       #
###############################################\n\n
===============================================
Sesión iniciada como {self.client.user.name}#{self.client.user.discriminator} | {self.client.user.id}
Ejecutandose en un {platform.system()} {platform.release()} ({os.name})
Versión de Python: {platform.python_version()}
Versión de Discord.py: {discord.__version__}
===============================================
Cargando cogs..."""
        )
        for cog in self.client.cogs_loaded:
            print(f" • Se ha cargado exitosamente el cog {cog}")
        print("===============================================")
        self.status_task.start()

    @tasks.loop(minutes=1)
    async def status_task(self) -> None:
        await self.client.change_presence(
            activity=discord.Game(random.choice(self.client.data["statuses"]))
        )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EventsCog(client))
