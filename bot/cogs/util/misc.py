import time

import discord
from discord import app_commands, Color
from discord.ext import commands, tasks
from discord.ext.commands import Context


class MiscUtil(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.snipes = dict[int, tuple[discord.Message, float]]()
        self.clear_snipes.start()

    @property
    def cog_unload(self):
        self.clear_snipes.cancel()

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if not message.author.bot and message.content:
            self.snipes[message.channel.id] = message, time.time()

    @tasks.loop(seconds=300)
    async def clear_snipes(self):
        for k, v in list(self.snipes.items()):
            if time.time() - v[1] > 5 * 60:
                try:
                    del self.snipes[k]
                except KeyError:
                    pass

    @commands.hybrid_command(name="ping", description="Obtiene la latencia actual del bot", aliases=["pong"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping_command(self, ctx: Context):
        start_time = time.time()
        ping_message = await ctx.send("Pong!")
        ping = round((time.time() - start_time) * 1000)
        embed = discord.Embed(description=f"Pong! {ping} ms.", color=Color.dark_green())
        await ping_message.edit(content=None, embed=embed)

    @commands.hybrid_command(
        name="math", description="Realiza operaciones matemáticas", aliases=["calc", "calculate", "calcula", "mat", "calculadora"]
    )
    @app_commands.describe(expresión="La operación que deseas resolver")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def math_command(self, ctx: Context, *, expresión: str):
        try:
            result = eval(expresión)
            embed = discord.Embed(
                description=f"{expresión} = {result}", color=Color.dark_green()
            )
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                description="¡Oops! No pude resolver esa operación.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="snipe", description="Muestra el último mensaje borrado")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def snipe_message(self, ctx: Context):
        snipe = self.snipes.pop(ctx.channel.id, None)

        if snipe is None:
            embed = discord.Embed(
                description="Parece que no hay nada que espíar.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)
        else:
            snipe, _ = snipe

            embed = discord.Embed(description=snipe.content, color=Color.dark_green())
            embed.set_author(
                name=str(snipe.author),
                icon_url=getattr(snipe.author.avatar, "url", None),
            )
            embed.timestamp = snipe.created_at

            await ctx.send(embed=embed)

    @commands.hybrid_command(name="avatar", description="Muestra el avatar de un usuario", aliases=["av"])
    @app_commands.describe(usuario="El usuario del que deseas mostrar el avatar")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def member_avatar(self, ctx: Context, usuario: discord.Member = None):
        user = usuario or ctx.author
        avatar_url = getattr(
            user.avatar,
            "url",
            "https://media.discordapp.net/attachments/643648150778675202/947881629047722064/gGWDJSghKgd8QAAAABJRU5ErkJggg.png",
        )

        embed = discord.Embed(
            description=f"Este es el avatar de {user.mention}.",
            color=Color.dark_green(),
        )
        embed.set_image(url=avatar_url)

        await ctx.reply(embed=embed, mention_author=False)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(MiscUtil(client))
