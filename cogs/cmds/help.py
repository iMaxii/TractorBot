import discord
from discord import Color, app_commands
from discord.ext import commands
from discord.ext.commands import Context
from reactionmenu import ViewButton, ViewMenu


class HelpCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_group(name="help")
    @app_commands.describe()
    async def help(self, ctx: Context) -> None:
        menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed, style="Página $/&")
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="Menú de ayuda",
                description=self.client.data["help"]["category"]["help1"],
                color=Color.dark_green(),
            )
            embed.add_field(
                name="**Tipos de comandos disponibles:**",
                value=self.client.data["help"]["category"]["help2"],
            )
            menu.add_page(embed)

            embed = discord.Embed(
                title="Comandos útiles",
                description=self.client.data["help"]["category"]["util"],
                color=Color.dark_green(),
            )
            menu.add_page(embed)

            embed = discord.Embed(
                title="Comandos tag",
                description=self.client.data["help"]["category"]["tag"],
                color=Color.dark_green(),
            )
            menu.add_page(embed)

            embed = discord.Embed(
                title="Comandos de diversión",
                description=self.client.data["help"]["category"]["fun"],
                color=Color.dark_green(),
            )
            menu.add_page(embed)

            first_button = ViewButton(
                emoji="⏪", custom_id=ViewButton.ID_GO_TO_FIRST_PAGE
            )
            back_button = ViewButton(emoji="◀️", custom_id=ViewButton.ID_PREVIOUS_PAGE)
            next_button = ViewButton(emoji="▶️", custom_id=ViewButton.ID_NEXT_PAGE)
            last_button = ViewButton(
                emoji="⏩", custom_id=ViewButton.ID_GO_TO_LAST_PAGE
            )
            menu.add_button(first_button)
            menu.add_button(back_button)
            menu.add_button(next_button)
            menu.add_button(last_button)
            menu.timeout = 300

            await menu.start()

    @help.command(base="help", name="util")
    async def help_tag(self, ctx: Context) -> None:
        embed = discord.Embed(
            title="Comandos útiles",
            description=self.client.data["help"]["category"]["util"],
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)

    @help.command(base="help", name="tag")
    async def help_util(self, ctx: Context) -> None:
        embed = discord.Embed(
            title="Comandos tag",
            description=self.client.data["help"]["category"]["tag"],
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)

    @help.command(base="help", name="fun")
    async def help_fun(self, ctx: Context) -> None:
        embed = discord.Embed(
            title="Comandos de diversión",
            description=self.client.data["help"]["category"]["fun"],
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)

    @help.command(base="help", name="command", aliases=["com", "c"])
    async def help_command(self, ctx: Context, *, command: str) -> None:
        if command in self.client.data["help"]["commands"]:
            embed = discord.Embed(
                title=f"!{command}",
                description=self.client.data["help"]["commands"][command],
                color=Color.dark_green(),
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"No se ha encontrado el commando {command}.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(HelpCog(client))
