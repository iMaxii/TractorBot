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
             .......\n            %@%%%%%@%\n        .  -=      =@     #%%%%%%# :%%%%%%%.      %%%      *%@@%# #%%%%%%#   %@@@%   :%%%%%%%.\n        +  @=::::::=@     #@@@@@@# :@@# #@@@:   ·@@@@@·  *@@@@@@# #@@@@@@#  %@@@@@%  :@@# #@@@:\n   .--=+#***********#.    #+@@@@+# :@@# #@@@:  .@@@ @@@. *@@@+    #+@@@@+# =@@@ @@@= :@@# #@@@:\n  #**********@@@@@@@@+      %@@%   :@@@@@@@:   %@@#=#@@% *@@@+      %@@%   =@@@ @@@= :@@@@@@@:\n @#*********@@*----*@@·     %@@%   :@@# #@@@: :@@@@@@@@@:*@@@@@@#   %@@%    %@@@@@%  :@@# #@@@:\n @#*@@*****@@*------*@@     %@@%   :@@# #@@@: =@@%. .%@@=  *%@@@#   %@@%     %@@@%   :@@# #@@@:\n  %@--@%####@@*----*@@·   \n   +@@+      +@@@@@@+
\n\n###############################################
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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if not message.guild:
            return
        if not message.content.startswith(
            self.client.config["prefix"]
        ) and not message.content.startswith(f"<@!{self.client.user.id}>"):
            if message.content.lower().startswith("saluda tractorbot"):
                await message.channel.send("Qué pasa chupabolas")
            else:
                return


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EventsCog(client))
