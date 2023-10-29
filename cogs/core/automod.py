import json
import os

import discord
from discord.ext import commands

links_path = (
    f"{os.path.realpath(os.path.dirname(__file__))}/../../data/banned_links.json"
)
words_path = (
    f"{os.path.realpath(os.path.dirname(__file__))}/../../data/banned_words.json"
)


class AutomodCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if not message.guild:
            return

        message_content = message.content.lower()
        banned_words = self.client.words["banned_words"]
        banned_links = self.client.links["bad_domains"]

        user = message.author

        if "discord.gg/" in message_content:
            await message.delete()
            embed = discord.Embed(
                color=0x925B5B, description=f"¡No puedes enviar invitaciones!"
            )
            await message.channel.send(embed=embed)

        for word in banned_words:
            if word in message_content:
                await message.delete()

        for link in banned_links:
            if link in message_content:
                guild = self.client.get_guild(self.client.config["guildid"])
                role = guild.get_role(self.client.config["vulneratedid"])
                await message.delete()
                embed = discord.Embed(
                    color=0x925B5B,
                    title="¡Alerta de seguridad!",
                    description=f"Hemos detectado que has enviado un link con un **dominio malicioso**, para más seguridad te hemos asignado el rol <@&1143938592155115591>. Te recomendamos que aumentes la seguridad de tu cuenta **cambiando la contraseña y activando la verificación en 2 pasos**, una vez lo hayas hecho puedes pedir que te quitemos el rol <@&1143938592155115591> en <#1143939908206076014>.",
                )
                await user.send(embed=embed)
                await user.add_roles(role)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AutomodCog(client))
