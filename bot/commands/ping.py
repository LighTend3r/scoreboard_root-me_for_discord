from discord import Interaction
from discord.app_commands import command, guilds
from discord.ext import commands
from utils.config import GUILD_ID


class PingCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ping")
    async def classic_ping(self, ctx: commands.Context) -> None:
        await ctx.send("pong")

    @command(name="ping")
    @guilds(GUILD_ID)
    async def slash_pong(self, interaction: Interaction):
        """Ping the bot"""
        await interaction.response.send_message("pong")


async def setup(client):
    await client.add_cog(PingCommand(client))
