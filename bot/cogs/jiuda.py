import discord
from discord.ext import commands
from discord import Color
import random
from discord.ext.commands import Context

class Jiuda(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="kill")
    async def kill(self, ctx: Context):
        rarities = self.client.data['jiuda']['rarities']
        x = round(random.uniform(0, 100), 2)

        acumulatedprob = 0

        for k, v in rarities.items():
            lower_prob = 100 - (acumulatedprob + v['probability'])
            higher_prob = 100 - acumulatedprob

            if lower_prob <= x < higher_prob:
                filtered_deaths = [d for d in self.client.data['jiuda']['deaths'] if d['rarity'] == k.lower()]
                death = random.choice(filtered_deaths)

                embed = discord.Embed(title=death['name'], description=death['event'], color=Color.dark_green())
                embed.set_footer(text=f"Puntos: {v['points']} | Rareza: {k.capitalize()}")

                await ctx.send(embed=embed)
                break
            acumulatedprob += v['probability']

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Jiuda(client))