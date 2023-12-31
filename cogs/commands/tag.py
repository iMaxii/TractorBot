import json
import os

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from reactionmenu import ViewButton, ViewMenu

from helpers import checks

tags_path = f"{os.path.realpath(os.path.dirname(__file__))}/../../data/tags.json"
with open(tags_path, encoding="utf-8") as file:
    tags = json.load(file)


class TagCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_group(name="tag")
    @app_commands.describe()
    @checks.not_blacklisted()
    async def tag(self, ctx: Context, *, tag: str) -> None:
        if ctx.invoked_subcommand is None:
            if tag in tags:
                await ctx.send(tags[tag]["content"])
            else:
                embed = discord.Embed(
                    color=0x925B5B, description=f"No se ha encontrado la tag {tag}."
                )
                await ctx.send(embed=embed)

    @tag.command(
        base="tag",
        name="add",
    )
    @checks.not_blacklisted()
    async def tag_add(self, ctx: Context, tag: str, *, content: str) -> None:
        if tag in tags:
            embed = discord.Embed(
                color=0x925B5B, description=f"La tag {tag} ya existe."
            )
            await ctx.send(embed=embed)
        else:
            tag_data = {"author_id": ctx.author.id, "content": content}
            tags[tag] = tag_data
            with open(tags_path, "w", encoding="utf-8") as f:
                json.dump(tags, f, indent=4)
            embed = discord.Embed(
                color=0x5B925F, description=f"Se ha creado con exito la tag {tag}."
            )
            await ctx.send(embed=embed)

    @tag.command(
        base="tag",
        name="edit",
    )
    @checks.not_blacklisted()
    async def tag_edit(self, ctx: Context, tag: str, *, content: str) -> None:
        if tag in tags:
            if ctx.author.id == tags[tag]["author_id"]:
                tags[tag]["content"] = content
                with open(tags_path, "w", encoding="utf-8") as f:
                    json.dump(tags, f, indent=4)
                embed = discord.Embed(
                    color=0x5B925F,
                    description=f"Se ha editado correctamente la tag {tag}.",
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    color=0x925B5B,
                    description=f"¡Oops! Parece que no eres dueño de la tag {tag}.",
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0x925B5B, description=f"No se ha encontrado la tag {tag}."
            )
            await ctx.send(embed=embed)

    @tag.command(base="tag", name="delete", aliases=["remove"])
    @checks.not_blacklisted()
    async def tag_delete(self, ctx: Context, *, tag: str) -> None:
        if tag in tags:
            if ctx.author.id == tags[tag]["author_id"]:
                del tags[tag]
                with open(tags_path, "w", encoding="utf-8") as f:
                    json.dump(tags, f, indent=4)
                embed = discord.Embed(
                    color=0x5B925F,
                    description=f"Se ha eliminado correctamente la tag {tag}.",
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    color=0x925B5B,
                    description=f"¡Oops! Parece que no eres dueño de la tag {tag}.",
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0x925B5B, description=f"No se ha encontrado la tag {tag}."
            )
            await ctx.send(embed=embed)

    @tag.command(base="tag", name="list")
    @checks.not_blacklisted()
    async def tag_list(self, ctx: Context) -> None:
        paginated_tags = [
            list(tags.items())[i : i + 20] for i in range(0, len(tags), 20)
        ]

        pages = []
        for index, tags_subset in enumerate(paginated_tags):
            tag_list = "\n".join(
                f"{index * 20 + i + 1}. {tag[0]}" for i, tag in enumerate(tags_subset)
            )
            embed = discord.Embed(color=0x59575A, title="Tags", description=tag_list)
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

    # A command to transfer the tag owner to another user
    @tag.command(base="tag", name="transfer")
    @checks.not_blacklisted()
    async def tag_transfer(self, ctx: Context, tag: str, user: discord.Member) -> None:
        if tag in tags:
            if ctx.author.id == tags[tag]["author_id"]:
                tags[tag]["author_id"] = user.id
                with open(tags_path, "w", encoding="utf-8") as f:
                    json.dump(tags, f, indent=4)
                embed = discord.Embed(
                    color=0x5B925F,
                    description=f"Se ha transferido correctamente la tag {tag} a {user.mention}.",
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    color=0x925B5B,
                    description=f"¡Oops! Parece que no eres dueño de la tag {tag}.",
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0x925B5B, description=f"No se ha encontrado la tag {tag}."
            )
            await ctx.send(embed=embed)

    # A command to see the info of a tag
    @tag.command(base="tag", name="info")
    @checks.not_blacklisted()
    async def tag_info(self, ctx: Context, *, tag: str) -> None:
        if tag in tags:
            author = await self.client.fetch_user(tags[tag]["author_id"])
            embed = discord.Embed(color=0x59575A)
            embed.set_author(name=tag, icon_url=ctx.guild.icon.url)
            embed.add_field(name="Contenido", value=f"```{tags[tag]['content']}```")
            embed.add_field(name="Autor", value=f"```{author}```")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0x925B5B, description=f"No se ha encontrado la tag {tag}."
            )
            await ctx.send(embed=embed)

    # Moderator only commands

    @tag.command(base="tag", name="forceedit", aliases=["fedit"])
    @checks.is_mod()
    @checks.not_blacklisted()
    async def tag_forceedit(self, ctx: Context, tag: str, *, content: str) -> None:
        if tag in tags:
            tags[tag]["content"] = content
            with open(tags_path, "w", encoding="utf-8") as f:
                json.dump(tags, f, indent=4)
            embed = discord.Embed(
                color=0x5B925F, description=f"Se ha editado correctamente la tag {tag}."
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0x925B5B, description=f"No se ha encontrado la tag {tag}."
            )
            await ctx.send(embed=embed)

    @tag.command(base="tag", name="forcedelete", aliases=["fdelete", "fremove"])
    @checks.is_mod()
    @checks.not_blacklisted()
    async def tag_forcedelete(self, ctx: Context, *, tag: str) -> None:
        if tag in tags:
            del tags[tag]
            with open(tags_path, "w", encoding="utf-8") as f:
                json.dump(tags, f, indent=4)
            embed = discord.Embed(
                color=0x5B925F,
                description=f"Se ha eliminado correctamente la tag {tag}.",
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=0x925B5B, description=f"No se ha encontrado la tag {tag}."
            )
            await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(TagCog(client))
