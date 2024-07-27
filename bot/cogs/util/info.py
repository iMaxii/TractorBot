import platform

import discord
from discord import Color
from discord.ext import commands, tasks
from discord.ext.commands import Context


class Info(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

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
            name="Dueño", value=f"```{(await self.client.application_info()).owner.name}```"
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
        embed.add_field(name="Licensia", value="```MIT License```")
        await ctx.send(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Info(client))