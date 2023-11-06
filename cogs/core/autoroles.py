import json
import os

import discord
from discord.ext import commands

from helpers import checks

config_path = f"{os.path.realpath(os.path.dirname(__file__))}/../../config.json"
with open(config_path) as file:
    config = json.load(file)


class Verification(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="✅", custom_id="Verify", style=discord.ButtonStyle.gray)
    async def verify(self, interaction, button):
        role = config["verifiedroleid"]
        user = interaction.user
        await user.add_roles(user.guild.get_role(role))


class AutorolesCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = self.client.get_guild(self.client.config["guildid"])
        role = guild.get_role(self.client.config["welcomeroleid"])
        channel = self.client.get_channel(self.client.config["welcomechannelid"])

        await member.add_roles(role)

        embed = discord.Embed(
            description=f"¡Bienvenido a **{guild}** {member.mention}!"
        )
        await channel.send(embed=embed)

    @checks.is_owner()
    @commands.command(name="verify")
    async def verify(self, ctx: commands.Context):
        embed = discord.Embed(
            title="¡Verificación!",
            description="Presiona el botón de abajo para ver el resto de canales.\nRecuerda revisar <#963085700448780319> para evitar posibles problemas.",
        )
        await ctx.send(embed=embed, view=Verification())


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AutorolesCog(client))
