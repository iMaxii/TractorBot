import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands import Context


class Sync(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx: Context) -> None:
        await ctx.bot.tree.sync()
        embed = discord.Embed(
            description="Se han sincronizado correctamente los comandos slash.",
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)
        return

    @commands.command(name="unsync")
    @commands.is_owner()
    async def unsync(self, ctx: Context) -> None:
        ctx.bot.tree.clear_commands(guild=None)
        await ctx.bot.tree.sync()
        embed = discord.Embed(
            description="Los comandos slash han sido desincronizados.",
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)
        return


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Sync(client))
