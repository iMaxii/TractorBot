import json
import os

import discord
from discord import app_commands, Color
from discord.ext import commands
from discord.ext.commands import Context
from reactionmenu import ViewButton, ViewMenu

links_path = f"{os.path.dirname(__file__)}/../../data/banned_links.json"


class BanLink(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_command(name="banlink", description="Agrega un link a la lista de links prohibidos", aliases=["bl", "banl"])
    @app_commands.describe(link="El link que deseas agregar")
    @commands.has_permissions(ban_members=True)
    async def banlink(self, ctx: Context, *, link: str):
        if link in self.client.links["bad_domains"]:
            embed = discord.Embed(
                description=f"Ese link ya está en la lista de links prohibidos.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)
        else:
            self.client.links["bad_domains"].append(link)
            with open(links_path, "w") as links_file:
                json.dump(self.client.links, links_file, indent=4)
            embed = discord.Embed(
                description=f"El link `{link}` ha sido añadido a la lista de links prohibidos.",
                color=Color.dark_green(),
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="unbanlink", description="Elimina un link de la lista de links prohibidos", aliases=["unbl", "unbanl"])
    @app_commands.describe(link="El link que deseas eliminar")
    @commands.has_permissions(ban_members=True)
    async def unbanlink(self, ctx: Context, *, link: str):
        if link in self.client.links["bad_domains"]:
            self.client.links["bad_domains"].remove(link)
            with open(links_path, "w") as links_file:
                json.dump(self.client.links, links_file, indent=4)
            embed = discord.Embed(
                description=f"El link `{link}` ha sido eliminado de la lista de links prohibidos.",
                color=Color.dark_green(),
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"Ese link no está en la lista de links prohibidos.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="bannedlinks", description="Muestra la lista de dominios baneados", aliases=["bllist", "bll"])
    @commands.has_permissions(ban_members=True)
    async def bannedlinks(self, ctx: Context):
        banned_links_list = self.client.links["bad_domains"]
        paginated_links = [
            banned_links_list[i : i + 20] for i in range(0, len(banned_links_list), 20)
        ]

        pages = []
        for index, links_subset in enumerate(paginated_links):
            bllist = "\n".join(
                f"{index * 20 + i + 1}. {bl}" for i, bl in enumerate(links_subset)
            )
            embed = discord.Embed(
                title="Lista de dominios baneados",
                description=bllist,
                color=Color.dark_green(),
            )
            pages.append(embed)

        menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed, style="Página $/&")

        for embed in pages:
            menu.add_page(embed)

        first_button = ViewButton(emoji="⏪", custom_id=ViewButton.ID_GO_TO_FIRST_PAGE)
        back_button = ViewButton(emoji="◀️", custom_id=ViewButton.ID_PREVIOUS_PAGE)
        next_button = ViewButton(emoji="▶️", custom_id=ViewButton.ID_NEXT_PAGE)
        last_button = ViewButton(emoji="⏩", custom_id=ViewButton.ID_GO_TO_LAST_PAGE)
        menu.add_button(first_button)
        menu.add_button(back_button)
        menu.add_button(next_button)
        menu.add_button(last_button)
        menu.timeout = 300

        await menu.start()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(BanLink(client))
