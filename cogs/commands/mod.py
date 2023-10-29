import json
import os

import discord
from discord.ext import commands
from reactionmenu import ViewButton, ViewMenu

from helpers import checks

words_path = (
    f"{os.path.realpath(os.path.dirname(__file__))}/../../data/banned_words.json"
)
links_path = (
    f"{os.path.realpath(os.path.dirname(__file__))}/../../data/banned_links.json"
)


class ModCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="banword", aliases=["bw", "banw"])
    @checks.is_mod()
    async def banword(self, ctx: commands.Context, *, word: str):
        if word in self.client.words["banned_words"]:
            embed = discord.Embed(
                color=0x925B5B,
                description=f"Esa palabra ya está en la lista de palabras prohibidas.",
            )
            await ctx.send(embed=embed)
        else:
            self.client.words["banned_words"].append(word)
            with open(words_path, "w") as file:
                json.dump(self.client.words, file, indent=4)
            embed = discord.Embed(
                color=0x5B925F,
                description=f"La palabra `{word}` ha sido añadida a la lista de palabras prohibidas.",
            )
            await ctx.send(embed=embed)

    @commands.command(name="unbanword", aliases=["unbw", "unbanw"])
    @checks.is_mod()
    async def unbanword(self, ctx: commands.Context, *, word: str):
        if word in self.client.words["banned_words"]:
            self.client.words["banned_words"].remove(word)
            with open(words_path, "w") as words_file:
                json.dump(self.client.words, words_file, indent=4)
            embed = discord.Embed(
                color=0x5B925F,
                description=f"La palabra `{word}` ha sido eliminada de la lista de palabras prohibidas.",
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0x925B5B,
                description=f"Esa palabra no está en la lista de palabras prohibidas.",
            )
            await ctx.send(embed=embed)

    @commands.command(name="bannedwords", aliases=["bwlist", "bwl"])
    @checks.is_mod()
    async def bannedwords(self, ctx: commands.Context):
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
                color=0x59575A, title="Lista de palabras baneadas", description=bwlist
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

    @commands.command(name="banlink", aliases=["bl", "banl"])
    @checks.is_mod()
    async def banlink(self, ctx: commands.Context, *, link: str):
        if link in self.client.links["bad_domains"]:
            embed = discord.Embed(
                color=0x925B5B,
                description=f"Ese link ya está en la lista de links prohibidos.",
            )
            await ctx.send(embed=embed)
        else:
            self.client.words["bad_domains"].append(link)
            with open(words_path, "w") as words_file:
                json.dump(self.client.words, words_file, indent=4)
            embed = discord.Embed(
                color=0x5B925F,
                description=f"El link `{link}` ha sido añadido a la lista de links prohibidos.",
            )
            await ctx.send(embed=embed)

    @commands.command(name="unbanlink", aliases=["unbl", "unbanl"])
    @checks.is_mod()
    async def unbanlink(self, ctx: commands.Context, *, link: str):
        if link in self.client.links["bad_domains"]:
            self.client.links["bad_domains"].remove(link)
            with open(words_path, "w") as words_file:
                json.dump(self.client.words, words_file, indent=4)
            embed = discord.Embed(
                color=0x5B925F,
                description=f"El link `{link}` ha sido eliminado de la lista de links prohibidos.",
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0x925B5B,
                description=f"Ese link no está en la lista de links prohibidos.",
            )
            await ctx.send(embed=embed)

    @commands.command(name="bannedlinks", aliases=["bllist", "bll"])
    @checks.is_mod()
    async def bannedlinks(self, ctx: commands.Context):
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
                color=0x59575A, title="Lista de dominios baneados", description=bllist
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
    await client.add_cog(ModCog(client))
