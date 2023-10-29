import discord
from discord.ext import commands
from discord.ext.commands import Context

import exceptions


class ErrorsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"¡Vaya! Parece que tienes que esperar {f'{round(hours)}h' if round(hours) > 0 else ''} {f'{round(minutes)}m' if round(minutes) > 0 else ''} {f'{round(seconds)}s' if round(seconds) > 0 else ''} antes de poder volver a utilizar ese comando.",
                color=0x925B5B,
            )
            await ctx.send(embed=embed)
        elif isinstance(error, exceptions.UserBlacklisted):
            return
        elif isinstance(error, exceptions.UserNotOwner):
            embed = discord.Embed(
                description="¡No eres el dueño del bot, por lo tanto no puedes utilizar ese comando!",
                color=0x925B5B,
            )
            await ctx.send(embed=embed)
        elif isinstance(error, exceptions.UserNotModerator):
            embed = discord.Embed(
                description="¡No eres moderador, por lo tanto no puedes utilizar ese comando!",
                color=0x925B5B,
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"¡Parece que te falta el permiso `{error.missing_permissions}` para ejecutar ese comando!",
                color=0x925B5B,
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description=f"¡Me falta el permiso `{error.missing_permissions}` para ejecutar correctamente ese comando!",
                color=0x925B5B,
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description="¡Parece que te faltan argumentos!", color=0x925B5B
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                description="¡Oops! No pude encontrar ese usuario.", color=0x925B5B
            )
            await ctx.send(embed=embed)
        else:
            if isinstance(error, commands.CommandNotFound):
                return
            else:
                errorc = self.client.get_channel(self.client.config["errorchannelid"])
                print(error)
                embed = discord.Embed(
                    description="¡Vaya! Parece que ha ocurrido un error al ejecutar ese comando.\nPor favor contacta a administración o abre un _issue_ en https://github.com/iMaxii/TractorBot",
                    color=0x925B5B,
                )

                await errorc.send(f"```py\n{error}\n```")
                await ctx.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(ErrorsCog(client))
