from typing import Any

import discord
from discord import Color, app_commands
from discord.ext import commands
from discord.ext.commands import Context

from bot.utils.pagination import paginate_embed


class Dropdown(discord.ui.Select):
    def __init__(self, pages):

        options = [
            discord.SelectOption(
                label="General",
                description="Muestra el menú de ayuda inicial",
                emoji="🚀",
            ),
            discord.SelectOption(
                label="Util",
                description="Muestra el menú de ayuda con los comandos de utilidad",
                emoji="🛠️",
            ),
            discord.SelectOption(
                label="Fun",
                description="Muestra el menú de ayuda con los comandos de diversión",
                emoji="🎉",
            ),
            discord.SelectOption(
                label="Tag",
                description="Muestra el menú de ayuda con los comandos tag",
                emoji="🏷️",
            ),
            discord.SelectOption(
                label="Jiuda",
                description="Muestra el menú de ayuda con los comandos de Jiuda",
                emoji="🗡️",
            ),
        ]

        self.pages = pages

        super().__init__(
            placeholder="Escoge un página del menú de ayuda",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.edit_message(
                embed=self.pages[self.values[0].lower()]
            )
        else:
            await interaction.followup.edit_message(
                interaction.message.id, embed=self.pages[self.values[0].lower()]
            )


class HelpCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    async def autocomplete_command(
        self, interaction: discord.Interaction, current: str
    ):
        client = interaction.client
        choices = []

        for category in client.data["help"]["commands"].values():
            for key in category.keys():
                if current.lower() in key.lower():
                    choices.append(app_commands.Choice(name=key, value=key))

        return choices

    async def autocomplete_category(
        self, interaction: discord.Interaction, current: str
    ):
        client = interaction.client
        choices = [
            app_commands.Choice(name=key, value=key)
            for key in client.data["help"]["categories"].keys()
            if current.lower() in key.lower()
        ]
        return choices

    def help_embed(
        self, *, type: str, command: str = None, name: str = None
    ) -> discord.Embed:
        if type == "general":
            embed = discord.Embed(
                title=self.client.data["help"]["categories"]["general"]["title"],
                description=self.client.data["help"]["categories"]["general"][
                    "description"
                ].format(prefix=self.client.config["prefix"]),
                color=Color.dark_green(),
            )
            for key, value in self.client.data["help"]["categories"]["general"][
                "fields"
            ].items():
                embed.add_field(
                    name=value["name"],
                    value=value["value"].format(
                        prefix=self.client.config["prefix"],
                        suggestions=self.client.config["suggestionschannelid"],
                        problems=self.client.config["supportchannelid"],
                    ),
                    inline=value["inline"],
                )
        elif type == "util":
            embed = discord.Embed(
                title=self.client.data["help"]["categories"]["util"]["title"],
                description=self.client.data["help"]["categories"]["util"][
                    "description"
                ],
                color=Color.dark_green(),
            )
            for key, value in self.client.data["help"]["categories"]["util"][
                "fields"
            ].items():
                embed.add_field(
                    name=value["name"],
                    value=f"{value['value']}\n".format(self.client.config["prefix"]),
                )
        elif type == "fun":
            embed = discord.Embed(
                title=self.client.data["help"]["categories"]["fun"]["title"],
                description=self.client.data["help"]["categories"]["fun"][
                    "description"
                ],
                color=Color.dark_green(),
            )
            for key, value in self.client.data["help"]["categories"]["fun"][
                "fields"
            ].items():
                embed.add_field(
                    name=value["name"],
                    value=value["value"].format(self.client.config["prefix"]),
                )
        elif type == "tag":
            embed = discord.Embed(
                title=self.client.data["help"]["categories"]["tag"]["title"],
                description=self.client.data["help"]["categories"]["tag"][
                    "description"
                ],
                color=Color.dark_green(),
            )
            for key, value in self.client.data["help"]["categories"]["tag"][
                "fields"
            ].items():
                embed.add_field(
                    name=value["name"],
                    value=value["value"].format(self.client.config["prefix"]),
                )
        elif type == "jiuda":
            embed = discord.Embed(
                title=self.client.data["help"]["categories"]["jiuda"]["title"],
                description=self.client.data["help"]["categories"]["jiuda"][
                    "description"
                ],
                color=Color.dark_green(),
            )
            for key, value in self.client.data["help"]["categories"]["jiuda"][
                "fields"
            ].items():
                embed.add_field(
                    name=value["name"],
                    value=value["value"].format(self.client.config["prefix"]),
                )
        elif type == "command":
            command_data = self.client.data["help"]["commands"]

            for cat, commands in command_data.items():
                if command in commands:
                    command_info = commands[command]
                    break

            if command_info:
                embed = discord.Embed(
                    title=command_info.get("title", f"{command}"),
                    description=command_info.get("description", ""),
                    color=Color.dark_green(),
                )
                if "usage" in command_info:
                    embed.description += f"\n{command_info['usage'].format(prefix=self.client.config['prefix'])}"
                if "field" in command_info:
                    embed.add_field(
                        name=command_info["field"]["name"].format(
                            prefix=self.client.config["prefix"]
                        ),
                        value=command_info["field"]["value"].format(
                            prefix=self.client.config["prefix"], mention=name
                        ),
                        inline=False,
                    )
            else:
                embed = discord.Embed(
                    description=f"No se encontró información para el comando `{command}`.",
                    color=Color.brand_red(),
                )
            embed.set_footer(
                text="Recuerda que también puedes utilizar los comandos con un /"
            )
        return embed

    @commands.hybrid_group(name="help")
    async def help(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            view = discord.ui.View()

            pages = {
                "general": self.help_embed(type="general"),
                "util": self.help_embed(type="util"),
                "fun": self.help_embed(type="fun"),
                "tag": self.help_embed(type="tag"),
                "jiuda": self.help_embed(type="jiuda"),
            }

            view.add_item(item=Dropdown(pages=pages))

            await ctx.send(embed=self.help_embed(type="general"), view=view)

    @help.command(name="category", description="Envía el menú de ayuda del bot.")
    @app_commands.describe(
        categoría="La categoría de la que deseas obtener información"
    )
    @app_commands.autocomplete(categoría=autocomplete_category)
    async def help_general(self, ctx: Context, categoría: str) -> None:
        c = categoría.lower()
        if c in self.client.data["help"]["categories"]:
            if c == "general":
                view = discord.ui.View()

                pages = {
                    "general": self.help_embed(type="general"),
                    "util": self.help_embed(type="util"),
                    "fun": self.help_embed(type="fun"),
                    "tag": self.help_embed(type="tag"),
                    "jiuda": self.help_embed(type="jiuda"),
                }

                view.add_item(item=Dropdown(pages=pages))

                await ctx.send(embed=self.help_embed(type="general"), view=view)
            else:
                if c != "command":
                    await ctx.send(embed=self.help_embed(type=c))
        else:
            embed = discord.Embed(
                description=f"No se ha encontrado la categoría {categoría}.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)

    @help.command(name="command", description="Envía información sobre un comando")
    @app_commands.describe(comando="El comando del que deseas obtener información")
    @app_commands.autocomplete(comando=autocomplete_command)
    async def help_command(self, ctx: Context, *, comando: str) -> None:
        await ctx.send(
            embed=self.help_embed(
                type="command",
                command=comando.lower(),
                name=(await self.client.application_info()).owner.name,
            )
        )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(HelpCog(client))
