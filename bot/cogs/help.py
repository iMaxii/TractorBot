import discord
from discord import app_commands, Color
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice

from bot.utils.pagination import paginate_embed

class HelpCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    async def autocomplete_commmand(self, interaction: discord.Interaction, current: str):
        client = interaction.client
        choices = [
            app_commands.Choice(name=key, value=key)
            for key in client.data["help"]["commands"].keys()
            if current.lower() in key.lower()
        ]
        return choices

    def help_embed(self, *, type: str, command: str = None) -> discord.Embed:
        if type == "general":
            embed = discord.Embed(title="Menú de ayuda", description=self.client.data["help"]["category"]["help1"], color=Color.dark_green())
            embed.add_field(name="**Tipos de comandos disponibles:**", value=self.client.data["help"]["category"]["help2"])
        elif type == "util":
            embed = discord.Embed(title="Comandos útiles", description=self.client.data["help"]["category"]["util"], color=Color.dark_green())
        elif type == "tag":
            embed = discord.Embed(title="Comandos tag", description=self.client.data["help"]["category"]["tag"], color=Color.dark_green())
        elif type == "fun":
            embed = discord.Embed(title="Comandos de diversión", description=self.client.data["help"]["category"]["fun"], color=Color.dark_green())
        elif type == "command":
            embed = discord.Embed(title=f"!{command}", description=self.client.data["help"]["commands"][command], color=Color.dark_green())
        return embed

    @commands.hybrid_group(name="help")
    async def help(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await paginate_embed(ctx, [self.help_embed(type="general"), self.help_embed(type="util"), self.help_embed(type="tag"), self.help_embed(type="fun")])

    @help.command(name="general", description="Envía el menú de ayuda del bot.")
    async def help_general(self, ctx: Context) -> None:
        await paginate_embed(ctx, [self.help_embed(type="general"), self.help_embed(type="util"), self.help_embed(type="tag"), self.help_embed(type="fun")])

    @help.command(name="util", description="Envía información sobre los comandos útiles")
    async def help_tag(self, ctx: Context) -> None:
        await ctx.send(embed=self.help_embed(type="util"))

    @help.command(name="tag", description="Envía información sobre los comandos tag")
    async def help_util(self, ctx: Context) -> None:
        await ctx.send(embed=self.help_embed(type="tag"))

    @help.command(name="fun", description="Envía información sobre los comandos de diversión")
    async def help_fun(self, ctx: Context) -> None:
        await ctx.send(embed=self.help_embed(type="fum"))

    @help.command(name="command", description="Envía información sobre un comando")
    @app_commands.describe(comando="El comando del que deseas obtener información")
    @app_commands.autocomplete(comando=autocomplete_commmand)
    async def help_command(self, ctx: Context, *, comando: str) -> None:
        if comando.lower() in self.client.data["help"]["commands"]:
            await ctx.send(embed=self.help_embed(type="command", command=comando))
        else:
            embed = discord.Embed(
                description=f"No se ha encontrado el commando {comando}.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)



async def setup(client: commands.Bot) -> None:
    await client.add_cog(HelpCog(client))
