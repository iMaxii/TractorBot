import json
import os

import discord
from discord import app_commands, Color
from discord.ext import commands
from discord.ext.commands import Context

from bot.utils.pagination import paginate_embed

words_path = f"{os.path.dirname(__file__)}/../../data/banned_words.json"


class BanWord(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_command(name="banword", description="Agrega una palabra o frase a la lista de palabras prohibidas", aliases=["bw", "banw"])
    @app_commands.describe(palabra="La palabra o frase que deseas agregar")
    @commands.has_permissions(ban_members=True)
    async def banword(self, ctx: Context, *, palabra: str):
        word = palabra.lower()
        if word in self.client.words["banned_words"]:
            embed = discord.Embed(
                description=f"Esa palabra ya está en la lista de palabras prohibidas.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)
        else:
            self.client.words["banned_words"].append(word)
            with open(words_path, "w") as file:
                json.dump(self.client.words, file, indent=4)
            embed = discord.Embed(
                description=f"La palabra `{word}` ha sido añadida a la lista de palabras prohibidas.",
                color=Color.dark_green(),
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="unbanword", description="Elimina una palabra o frase de la lista de palabras prohibidas", aliases=["unbw", "unbanw"])
    @app_commands.describe(palabra="La palabra o frase que deseas eliminar")
    @commands.has_permissions(ban_members=True)
    async def unbanword(self, ctx: Context, *, palabra: str):
        word = palabra.lower()
        if word in self.client.words["banned_words"]:
            self.client.words["banned_words"].remove(word)
            with open(words_path, "w") as words_file:
                json.dump(self.client.words, words_file, indent=4)
            embed = discord.Embed(
                description=f"La palabra `{word}` ha sido eliminada de la lista de palabras prohibidas.",
                color=Color.dark_green(),
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"Esa palabra no está en la lista de palabras prohibidas.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="bannedwords", description="Muestra la lista de palabras prohibidas", aliases=["bwlist", "bwl"])
    @commands.has_permissions(ban_members=True)
    async def bannedwords(self, ctx: Context):
        bw_list = self.client.words["banned_words"]
        paginated_words = [
            bw_list[i : i + 20] for i in range(0, len(self.client.words), 20)
        ]

        pages = []
        for index, words_subset in enumerate(paginated_words):
            bwlist = "\n".join(
                f"{index * 20 + i + 1}. {bw}" for i, bw in enumerate(words_subset)
            )
            embed = discord.Embed(
                title="Lista de palabras baneadas",
                description=bwlist,
                color=Color.dark_green(),
            )
            pages.append(embed)

        await paginate_embed(ctx, pages)

async def setup(client):
    await client.add_cog(BanWord(client))