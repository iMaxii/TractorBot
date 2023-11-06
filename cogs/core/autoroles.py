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


class Autoroles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        emoji="🥥",
        style=discord.ButtonStyle.gray,
        custom_id="Updates",
    )
    async def updates(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        user = interaction.user
        role = user.guild.get_role(1171175790923223122)
        if role.id in [y.id for y in user.roles]:
            await interaction.response.send_message(
                f"Se te ha quitado el rol **🥥╏Actualizaciones**. Ya no se te notificará cada vez que haya un cumpleaños.",
                ephemeral=True,
            )
            await user.remove_roles(role)
        else:
            await interaction.response.send_message(
                "¡Ya tienes el rol **🥥╏Actualizaciones**! Ahora se te notificará cada vez que haya una actualización.",
                ephemeral=True,
            )
            await user.add_roles(role)

    @discord.ui.button(emoji="🍍", style=discord.ButtonStyle.gray, custom_id="Events")
    async def events(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        role = user.guild.get_role(1171175736086896710)
        if role.id in [y.id for y in user.roles]:
            await interaction.response.send_message(
                f"Se te ha quitado el rol **🍍╏Eventos**. Ya no se te notificará cada vez que haya un cumpleaños.",
                ephemeral=True,
            )
            await user.remove_roles(role)
        else:
            await interaction.response.send_message(
                "¡Ya tienes el rol **🍍╏Eventos**! Ahora se te notificará cada vez que haya un evento.",
                ephemeral=True,
            )
            await user.add_roles(role)

    @discord.ui.button(emoji="🥝", style=discord.ButtonStyle.gray, custom_id="Birthdays")
    async def birthdays(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        user = interaction.user
        role = user.guild.get_role(1171175844408987699)
        if role.id in [y.id for y in user.roles]:
            await interaction.response.send_message(
                f"Se te ha quitado el rol **🥝╏Cumpleaños**. Ya no se te notificará cada vez que haya un cumpleaños.",
                ephemeral=True,
            )
            await user.remove_roles(role)
        else:
            await interaction.response.send_message(
                f"¡Ya tienes el rol **🥝╏Cumpleaños**! Ahora se te notificará cada vez que haya un cumpleaños.",
                ephemeral=True,
            )
            await user.add_roles(role)


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

    @checks.is_owner()
    @commands.command(name="autoroles")
    async def autoroles(self, ctx: commands.Context):
        embed = discord.Embed(
            title="¡Autoroles!",
            description="Presiona el botón que tiene un:\n- 🥥 Para recibir el rol **Actualizaciones**. ¡Con este rol se te notificara cada vez que haya una actualización en el servidor!\n- 🍍 Para recibir el rol **Eventos**. ¡Con este rol se te notificara cada vez que haya un evento en el servidor!\n- 🥝 Para recibir el rol **Cumpleaños**. ¡Con este rol se te notificara cada vez que haya un cumpleaños en el servidor!",
        )
        await ctx.send(embed=embed, view=Autoroles())


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AutorolesCog(client))
