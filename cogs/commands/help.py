import json
import os

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from reactionmenu import ViewButton, ViewMenu

from helpers import checks


class HelpCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_group(name="help")
    @app_commands.describe()
    @checks.not_blacklisted()
    async def help(self, ctx: Context) -> None:
        menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed, style="Página $/&")
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                color=0x59575A,
                title="Menú de ayuda",
                description=self.client.data["help"]["category"]["help1"],
            )
            embed.add_field(
                name="**Tipos de comandos disponibles:**",
                value=self.client.data["help"]["category"]["help2"],
            )
            menu.add_page(embed)

            embed = discord.Embed(
                title="Comandos útiles",
                color=0x59575A,
                description=self.client.data["help"]["category"]["util"],
            )
            menu.add_page(embed)

            embed = discord.Embed(
                title="Comandos tag",
                color=0x59575A,
                description=self.client.data["help"]["category"]["tag"],
            )
            menu.add_page(embed)

            embed = discord.Embed(
                title="Comandos de diversión",
                color=0x59575A,
                description=self.client.data["help"]["category"]["fun"],
            )
            menu.add_page(embed)

            first_button = ViewButton(
                emoji="⏪", custom_id=ViewButton.ID_GO_TO_FIRST_PAGE
            )
            back_button = ViewButton(emoji="◀️", custom_id=ViewButton.ID_PREVIOUS_PAGE)
            next_button = ViewButton(emoji="▶️", custom_id=ViewButton.ID_NEXT_PAGE)
            last_button = ViewButton(emoji="⏩", custom_id=ViewButton.ID_GO_TO_LAST_PAGE)
            menu.add_button(first_button)
            menu.add_button(back_button)
            menu.add_button(next_button)
            menu.add_button(last_button)
            menu.timeout = 300

            await menu.start()

    @help.command(base="help", name="util")
    @checks.not_blacklisted()
    async def help_tag(self, ctx: Context) -> None:
        embed = discord.Embed(
            title="Comandos útiles",
            color=0x59575A,
            description=self.client.data["help"]["category"]["util"],
        )
        await ctx.send(embed=embed)

    @help.command(base="help", name="tag")
    @checks.not_blacklisted()
    async def help_util(self, ctx: Context) -> None:
        embed = discord.Embed(
            title="Comandos tag",
            color=0x59575A,
            description=self.client.data["help"]["category"]["tag"],
        )
        await ctx.send(embed=embed)

    @help.command(base="help", name="fun")
    @checks.not_blacklisted()
    async def help_fun(self, ctx: Context) -> None:
        embed = discord.Embed(
            title="Comandos de diversión",
            color=0x59575A,
            description=self.client.data["help"]["category"]["fun"],
        )
        await ctx.send(embed=embed)

    @help.command(base="help", name="command", aliases=["com", "c"])
    @checks.not_blacklisted()
    async def help_command(self, ctx: Context, *, command: str) -> None:
        if command in self.client.data["help"]["commands"]:
            embed = discord.Embed(
                color=0x59575A,
                title=f"!{command}",
                description=self.client.data["help"]["commands"][command],
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0x925B5B,
                description=f"No se ha encontrado el commando {command}.",
            )
            await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(HelpCog(client))
