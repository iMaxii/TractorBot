import discord
from discord import Color, app_commands
from discord.ext import commands
from discord.ext.commands import Context


class MiscOwner(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_command(name="coglist", description="Lista los cogs del bot.")
    @commands.is_owner()
    async def coglist(self, ctx: Context) -> None:
        coglist = "\n- ".join(cog for cog in self.client.cogs_loaded)
        embed = discord.Embed(
            title="Lista de Cogs existentes:",
            description=f"- {coglist}",
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="shutdown", description="Apaga el bot.")
    @commands.is_owner()
    async def shutdown(self, ctx: Context) -> None:
        embed = discord.Embed(
            description="¡Apagando, adios! :wave:", color=Color.gold()
        )
        await ctx.send(embed=embed)
        await self.client.close()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(MiscOwner(client))
