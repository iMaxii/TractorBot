import platform
import time

import discord
from discord import Color
from discord.ext import commands, tasks
from discord.ext.commands import Context


class UtilCog(commands.Cog):
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

    @commands.command(
        name="ping", aliases=["pong"], help="Obtiene la latencia actual del bot"
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping_command(self, ctx: Context):
        start_time = time.time()
        ping_message = await ctx.send("Pong!")
        ping = round((time.time() - start_time) * 1000)
        embed = discord.Embed(description=f"Pong! {ping} ms.", color=Color.dark_green())
        await ping_message.edit(content=None, embed=embed)

    @commands.command(
        name="math", aliases=["calc", "calculate", "calcula", "mat", "calculadora"]
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def math_command(self, ctx: Context, *, equation: str):
        try:
            result = eval(equation)
            embed = discord.Embed(
                description=f"{equation} = {result}", color=Color.dark_green()
            )
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                description="¡Oops! No pude resolver esa operación.",
                color=Color.brand_red(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="snipe")
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

    @commands.command(name="avatar", aliases=["av"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def member_avatar(self, ctx: Context, member: discord.Member = None):
        user = member or ctx.author
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

    @commands.command(name="userinfo", aliases=["ui", "info", "whois", "who"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def userinfo(self, ctx: Context, member: discord.Member = None):
        user = member or ctx.author
        embed = discord.Embed(color=Color.dark_green())
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.add_field(name="Nombre", value=f"```{user.name}```")
        embed.add_field(name="Nombre de usuario", value=f"```{user.display_name}```")
        embed.add_field(name="ID", value=f"```{user.id}```")
        embed.add_field(
            name="Cuenta creada",
            value=f"```{user.created_at.strftime('%d/%m/%Y %H:%M:%S')}```",
            inline=True,
        )
        embed.add_field(
            name="Se unió",
            value=f"```{user.joined_at.strftime('%d/%m/%Y %H:%M:%S')}```",
            inline=True,
        )
        if len(user.roles) > 1:
            embed.add_field(
                name="Roles",
                value=", ".join(
                    [role.mention for role in user.roles if role.name != "@everyone"]
                ),
                inline=False,
            )
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=["si", "server", "guildinfo", "guild"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def serverinfo(self, ctx: Context):
        embed = discord.Embed(color=Color.dark_green())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed.add_field(name="Nombre", value=f"```{ctx.guild.name}```")
        embed.add_field(name="ID", value=f"```{ctx.guild.id}```")
        embed.add_field(
            name="Creado",
            value=f"```{ctx.guild.created_at.strftime('%d/%m/%Y %H:%M:%S')}```",
        )
        embed.add_field(
            name="Miembros", value=f"```{ctx.guild.member_count}```", inline=True
        )
        embed.add_field(
            name="Roles", value=f"```{len(ctx.guild.roles)}```", inline=True
        )
        embed.add_field(
            name="Emojis", value=f"```{len(ctx.guild.emojis)}```", inline=True
        )
        if ctx.guild.premium_subscription_count != 0:
            embed.add_field(
                name="Boosts",
                value=f"```{ctx.guild.premium_subscription_count}```",
                inline=True,
            )
            embed.add_field(
                name="Nivel de boost",
                value=f"```{ctx.guild.premium_tier}```",
                inline=True,
            )
        embed.add_field(name="Dueño", value=ctx.guild.owner.mention, inline=True)
        embed.add_field(
            name="Administradores",
            value=" ".join(
                [
                    admin.mention
                    for admin in ctx.guild.members
                    if admin.guild_permissions.administrator
                    and not admin.bot
                    and admin != ctx.guild.owner
                ]
            ),
        )
        embed.add_field(
            name="Moderadores",
            value=" ".join(
                [
                    mod.mention
                    for mod in ctx.guild.members
                    if mod.guild_permissions.kick_members
                    and not mod.guild_permissions.administrator
                    and not mod.bot
                ]
            ),
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command(name="botinfo", aliases=["bi", "bot"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def botinfo(self, ctx: Context):
        ownerid = self.client.config["ownerid"][0]
        embed = discord.Embed(color=Color.dark_green())
        embed.set_author(
            name=self.client.user.name, icon_url=self.client.user.avatar.url
        )
        embed.add_field(name="Nombre", value=f"```{self.client.user.name}```")
        embed.add_field(name="ID", value=f"```{self.client.user.id}```")
        embed.add_field(
            name="Creado",
            value=f"```{self.client.user.created_at.strftime('%d/%m/%Y %H:%M:%S')}```",
        )
        embed.add_field(
            name="Dueño", value=f"```{self.client.get_user(ownerid).name}```"
        )
        embed.add_field(
            name="Versión de discord.py", value=f"```{discord.__version__}```"
        )
        embed.add_field(
            name="Versión de Python", value=f"```{platform.python_version()}```"
        )
        embed.add_field(
            name="Código fuente", value="```https://github.com/iMaxii/TractorBot```"
        )
        embed.add_field(name="Licensia", value="```GNU General Public License v3.0```")
        await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(UtilCog(client))
