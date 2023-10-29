import os
import platform
import random

import discord
from discord.ext import commands, tasks


class EventsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"""
             .......\n            %@%%%%%@%\n        .  -=      =@     #%%%%%%# :%%%%%%%.      %%%      *%@@%# #%%%%%%#   %@@@%   :%%%%%%%.\n        +  @=::::::=@     #@@@@@@# :@@# #@@@:   ·@@@@@·  *@@@@@@# #@@@@@@#  %@@@@@%  :@@# #@@@:\n   .--=+#***********#.    #+@@@@+# :@@# #@@@:  .@@@ @@@. *@@@+    #+@@@@+# =@@@ @@@= :@@# #@@@:\n  #**********@@@@@@@@+      %@@%   :@@@@@@@:   %@@#=#@@% *@@@+      %@@%   =@@@ @@@= :@@@@@@@:\n @#*********@@*----*@@·     %@@%   :@@# #@@@: :@@@@@@@@@:*@@@@@@#   %@@%    %@@@@@%  :@@# #@@@:\n @#*@@*****@@*------*@@     %@@%   :@@# #@@@: =@@%. .%@@=  *%@@@#   %@@%     %@@@%   :@@# #@@@:\n  %@--@%####@@*----*@@·   \n   +@@+      +@@@@@@+
\n\n###############################################
#              Bot made by iMaxii             #
#          https://github.com/iMaxii          # 
#                                             #
#         Join The Tractor Army Discord       #
#         https://discord.gg/74SJhxT6Nt       #
###############################################\n\n
===============================================
Logged in as {self.client.user.name}#{self.client.user.discriminator} | {self.client.user.id}
Running on {platform.system()} {platform.release()} ({os.name})
Python Version: {platform.python_version()}
Discord.py Version: {discord.__version__}
===============================================
Loading cogs..."""
        )
        for ext in self.client.cogslist:
            if ext.startswith("cogs.commands"):
                print(f"Loaded {ext.replace('cogs.commands.', '')} cog")
            else:
                print(f"Loaded {ext.replace('cogs.core.', '')} cog")
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
            if message.content.startswith("Saluda TractorBot".lower()):
                await message.channel.send("Qué pasa chupabolas")
            else:
                return


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EventsCog(client))
