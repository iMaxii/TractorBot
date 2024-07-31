import random

import discord
from discord import app_commands, Color
from discord.ext import commands
from discord.ext.commands import Context


class FunCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_command(name="gayrate", description="Mide el nivel de homosexualidad de un usuario o algo", aliases=["gay", "homo", "homosexualidad"])
    @app_commands.describe(usuario="El usuario o algo del que queramos medir el nivel de homosexualidad")
    async def gayrate_command(self, ctx: Context, *, usuario: str = "") -> None:
        if usuario == "":
            user = ctx.author.display_name
            rate = random.randint(0, 100)
            embed = discord.Embed(
                description=f"{user} es un {rate}% gay", color=Color.dark_green()
            )
            await ctx.send(embed=embed)
        else:
            try:
                mention = ctx.message.mentions[0]
                user = mention.display_name
                rate = random.randint(0, 100)
                embed = discord.Embed(
                    description=f"{user} es un {rate}% gay",
                    color=Color.dark_green(),
                )
                await ctx.send(embed=embed)
            except IndexError:
                rate = random.randint(0, 100)
                embed = discord.Embed(
                    description=f"{usuario} es un {rate}% gay", color=Color.dark_green()
                )
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="say", description="El bot dirá lo que quieras", aliases=["di"])
    @app_commands.describe(mensaje="El mensaje que deseas enviar")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def say_command(self, ctx: Context, *, mensaje: str):
        await ctx.send(mensaje)

    @commands.hybrid_command(name="8ball", description="Preguntale a la bola 8 lo que quieras", aliases=["fortune", "ask", "bola8"])
    @app_commands.describe(pregunta="La pregunta que deseas hacer")
    async def eight_ball_command(self, ctx: Context, *, pregunta: str):
        responses = self.client.data["8ball"]
        embed = discord.Embed(
            title=pregunta.lower().capitalize(),
            description=random.choice(responses),
            color=Color.dark_green(),
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="owo", description="Owofica el texto que quieras", aliases=["owofy", "owofica", "uwu"])
    @app_commands.describe(texto="El texto que deseas owoficar")
    async def owo(self, ctx: Context, *, texto: str):
        owos = self.client.data["owos"]
        texto = texto.lower().replace("l", "w").replace("r", "w").replace("n", "ñ")
        await ctx.send(f"{texto} {random.choice(owos)}")

    @commands.hybrid_command(name="facts", description="Envía un dato aleatorio", aliases=["fact", "randomfacts", "tractorfacts"])
    async def facts_command(self, ctx: Context):
        facts = self.client.data["facts"]
        embed = discord.Embed(
            description=random.choice(facts), color=Color.dark_green()
        )
        await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(FunCog(client))
