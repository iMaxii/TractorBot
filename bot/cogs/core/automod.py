import os

import discord
from discord import Color
from discord.ext import commands

links_path = f"{os.path.dirname(__file__)}/../../data/banned_links.json"
words_path = f"{os.path.dirname(__file__)}/../../data/banned_words.json"


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
                description=f"¡No puedes enviar invitaciones!", color=Color.brand_red()
            )
            await message.channel.send(embed=embed)

        for word in banned_words:
            if word in message_content:
                await message.delete()

        for link in banned_links:
            if link in message_content:
                guild = self.client.get_guild(self.client.config["guildid"])
                role = guild.get_role(self.client.config["vulneratedroleid"])
                await message.delete()
                embed = discord.Embed(
                    description=f"Hemos detectado que has enviado un enlace con un dominio malicioso.\nPara garantizar la seguridad de tu cuenta, te recomendamos que cambies tu contraseña y actives la verificación en dos pasos. Una vez hayas completado estos pasos, puedes solicitar asistencia en el canal <#{self.client.config['vulneratedchannelid']}>.",
                    color=Color.brand_red(),
                )
                await user.send(embed=embed)
                await user.add_roles(role)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AutomodCog(client))
