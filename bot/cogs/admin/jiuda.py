import json
import os

import discord
from discord import Color, app_commands
from discord.ext import commands
from discord.ext.commands import Context

data_path = f"{os.path.dirname(__file__)}/../../data"


class JiudaAdmin(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def autocomplete_rarity(self, interaction: discord.Interaction, current: str):
        client = interaction.client
        choices = [
            app_commands.Choice(name=key, value=key)
            for key in client.data["jiuda"]["rarities"].keys()
            if current.lower() in key.lower()
        ]
        return choices

    @commands.hybrid_command(name="adddeath", description="Añade una muerte")
    @commands.has_permissions(administrator=True)
    @app_commands.describe(
        rarity="Rareza de la muerte",
        id="ID de la muerte",
        details="Nombre y evento de la muerte",
    )
    @app_commands.autocomplete(rarity=autocomplete_rarity)
    async def adddeath(self, ctx: Context, rarity: str, id: str, *, details: str):
        if rarity.lower() not in self.client.data["jiuda"]["rarities"].keys():
            embed = discord.Embed(
                description=f"La rareza {rarity.lower()} no existe, debe ser una de las siguientes: {', '.join(self.client.data['jiuda']['rarities'].keys())}.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)
            return

        if id.lower() in [death["id"] for death in self.client.data["jiuda"]["deaths"]]:
            embed = discord.Embed(
                description=f"Ya hay una muerte con la id {id.lower()}.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)
            return

        try:
            name, event = details.split("|")
        except ValueError:
            embed = discord.Embed(
                description="Debes especificar un nombre y un evento, y separarlos con el simbolo `|`.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)
            return

        name, event = name.strip(), event.strip()

        death_entry = {
            "id": id.lower(),
            "name": name,
            "event": event,
            "rarity": rarity.lower(),
        }

        self.client.data["jiuda"]["deaths"].append(death_entry)
        with open(f"{data_path}/data.json", "w", encoding="utf-8") as f:
            json.dump(self.client.data, f, indent=4, ensure_ascii=False)

        embed = discord.Embed(
            description="Se ha añadido la muerte correctamente.",
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(JiudaAdmin(client))
