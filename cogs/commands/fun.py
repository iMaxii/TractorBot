import json
import os
import random

import discord
import requests
from discord.ext import commands
from reactionmenu import ViewButton, ViewMenu

from helpers import checks


class FunCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @checks.not_blacklisted()
    @commands.command(name="gayrate", aliases=["gay", "homo", "homosexualidad"])
    async def gayrate_command(self, ctx: commands.Context, *, arg=""):
        user_id = 728016426228514896
        if ctx.message.mentions and ctx.message.mentions[0].id == user_id:
            user = ctx.message.mentions[0].display_name
            rate = random.randint(100, 300)
            embed = discord.Embed(
                color=0x59575A, description=f"{user} es un {rate}% gay"
            )
            await ctx.send(embed=embed)

        else:
            if arg == "":
                user = ctx.author.display_name
                rate = random.randint(0, 100)
                embed = discord.Embed(
                    color=0x59575A, description=f"{user} es un {rate}% gay"
                )
                await ctx.send(embed=embed)
            else:
                try:
                    mention = ctx.message.mentions[0]
                    user = mention.display_name
                    rate = random.randint(0, 100)
                    embed = discord.Embed(
                        color=0x59575A, description=f"{user} es un {rate}% gay"
                    )
                    await ctx.send(embed=embed)
                except IndexError:
                    rate = random.randint(0, 100)
                    embed = discord.Embed(
                        color=0x59575A, description=f"{arg} es un {rate}% gay"
                    )
                    await ctx.send(embed=embed)

    @checks.not_blacklisted()
    @commands.command(name="say", aliases=["di"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def say_command(self, ctx: commands.Context, *, message: str):
        await ctx.send(message)

    @checks.not_blacklisted()
    @commands.command(name="8ball", aliases=["fortune", "ask", "bola8"])
    async def eight_ball_command(self, ctx: commands.Context, *, question: str):
        responses = self.client.data["8ball"]
        embed = discord.Embed(
            title=question.capitalize(),
            description=random.choice(responses),
            color=0x59575A,
        )
        await ctx.send(embed=embed)

    @checks.not_blacklisted()
    @commands.command(name="owo", aliases=["owofy", "owofica", "uwu"])
    async def owo(self, ctx: commands.Context, *, text: str):
        owos = self.client.data["owos"]
        text = text.lower().replace("l", "w").replace("r", "w").replace("n", "ñ")
        await ctx.send(f"{text} {random.choice(owos)}")

    @checks.not_blacklisted()
    @commands.command(name="facts", aliases=["fact", "randomfacts", "tractorfacts"])
    async def facts_command(self, ctx: commands.Context):
        facts = self.client.data["facts"]
        embed = discord.Embed(color=0x59575A, description=random.choice(facts))
        await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(FunCog(client))
