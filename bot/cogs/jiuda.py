import random

import discord
from discord import Color, app_commands
from discord.ext import commands
from discord.ext.commands import Context

import bot.utils.db_manager as db
from bot.utils.pagination import paginate_embed


class Jiuda(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(
        name="kill", description="Mata a Jiuda y obtén puntos", aliases=["matar"]
    )
    async def kill(self, ctx: Context):
        rarities = self.client.data["jiuda"]["rarities"]
        x = round(random.uniform(0, 100), 2)

        acumulatedprob = 0

        for k, v in rarities.items():
            lower_prob = 100 - (acumulatedprob + v["probability"])
            higher_prob = 100 - acumulatedprob

            if lower_prob <= x < higher_prob:
                filtered_deaths = [
                    d
                    for d in self.client.data["jiuda"]["deaths"]
                    if d["rarity"] == k.lower()
                ]
                death = random.choice(filtered_deaths)

                embed = discord.Embed(
                    title=death["name"],
                    description=death["event"],
                    color=Color.dark_green(),
                )
                embed.set_footer(
                    text=f"Puntos: {v['points']} | Rareza: {k.capitalize()}"
                )

                await db.add_death(ctx.author.id, death["id"], v["points"])
                await ctx.send(embed=embed)

                break
            acumulatedprob += v["probability"]

    @commands.hybrid_command(
        name="deaths", description="Muestra tus muertes obtenidas", aliases=["muertes"]
    )
    async def deaths(self, ctx: Context):
        deaths = await db.get_user_deaths(ctx.author.id)

        if len(deaths) == 0:
            embed = discord.Embed(
                description=f"{ctx.author.display_name} no tiene muertes registradas",
                color=Color.brand_red,
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(color=Color.dark_green())
        embed.set_author(
            name=f"Muertes de {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        pages = []
        for i, d in enumerate(deaths):
            death = [
                death
                for death in self.client.data["jiuda"]["deaths"]
                if death["id"] == d[0]
            ]
            death = death[0]
            embed.add_field(
                name=death["name"],
                value=f"ID: {d[0].capitalize()} | Rareza: {death['rarity'].capitalize()}",
                inline=False,
            )
            if (i + 1) % 7 == 0 or i + 1 == len(deaths):
                pages.append(embed)
                if i + 1 < len(deaths):
                    embed = discord.Embed(color=Color.dark_green())
                    embed.set_author(
                        name=f"Muertes de {ctx.author.display_name}",
                        icon_url=ctx.author.display_avatar.url,
                    )

        if len(pages) <= 1:
            await ctx.send(embed=embed)
        else:
            await paginate_embed(ctx, pages)

    @commands.hybrid_command(
        name="deathinfo",
        description="Muestra la informacion de una muerte",
        aliases=["dinfo", "death", "muerte"],
    )
    @app_commands.describe(death_id="La ID de la muerte")
    async def deathinfo(self, ctx: Context, death_id: str):
        death = [
            death
            for death in self.client.data["jiuda"]["deaths"]
            if death["id"] == death_id.lower()
        ]
        if len(death) == 0:
            embed = discord.Embed(
                description="No se ha encontrado la muerte", color=Color.brand_red()
            )
            await ctx.send(embed=embed)
            return

        death = death[0]
        embed = discord.Embed(
            title=death["name"], description=death["event"], color=Color.dark_green()
        )
        embed.set_footer(
            text=f"Rareza: {death['rarity'].capitalize()} | Puntos: {self.client.data['jiuda']['rarities'][death['rarity']]['points']}"
        )
        await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Jiuda(client))
