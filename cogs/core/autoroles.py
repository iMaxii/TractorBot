import discord
import reactionmenu
from discord.ext import commands


class AutorolesCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = self.client.get_guild(self.client.config["guildid"])
        role = guild.get_role(self.client.config["welcomeroleid"])
        channel = self.client.get_channel(self.client.config["welcomechannelid"])

        await member.add_roles(role)

        embed = discord.Embed(
            description=f"¡Bienvenido a **{guild}** {member.mention}!"
        )
        await channel.send(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AutorolesCog(client))
