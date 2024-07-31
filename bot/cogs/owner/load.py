import discord
from discord import Color, app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Load(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_command(name="load", description="Carga un cog.")
    @app_commands.describe(cog="El nombre del cog a cargar")
    @commands.is_owner()
    async def load(self, ctx: Context, cog: str) -> None:
        try:
            await self.client.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"No se ha podido cargar el cog `{cog}`.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Se ha cargado correctamente el cog `{cog}`.",
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="unload", description="Descarga un cog.")
    @app_commands.describe(cog="El nombre del cog a descargar")
    @commands.is_owner()
    async def unload(self, ctx: Context, cog: str) -> None:
        try:
            await self.client.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"No se ha podido descargar el cog `{cog}`.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Se ha descargado correctamente el cog `{cog}`.",
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="reload", description="Recarga un cog.")
    @app_commands.describe(cog="El nombre del cog a recargar")
    @commands.is_owner()
    async def reload(self, ctx: Context, cog: str) -> None:
        try:
            await self.client.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"No se ha podido recargar el cog `{cog}`.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Se ha recargado correctamente el cog `{cog}`.",
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Load(client))
