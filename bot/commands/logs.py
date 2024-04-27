import discord
import discord.app_commands.errors as app_errors
from discord import Interaction
from discord.app_commands import command, guilds
from discord.ext import commands
from discord.ext.commands.errors import (
    MissingAnyRole,
    MissingRequiredArgument,
    UserNotFound,
)
from utils.config import (
    TEMP_LOG_FILENAME,
    GUILD_ID
)

import utils.logging as logging_error


class LogsCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.error_embed = discord.Embed(
            description="""Command usage:
            ``/logs [size]``

            **Arguments:**
            ``size``: Integer specifying the number of lines to show
            """,
            color=0xFF0000,
        )

    @command(name="logs")
    @guilds(GUILD_ID)
    async def slash_logs(
        self, interaction: discord.Interaction, number: int = 10
    ) -> None:
        """Display latest logs form discord bot"""
        message = await self.logs_impl(number)
        if type(message) == discord.Embed:
            await interaction.response.send_message(embed=message)
        else:
            await interaction.response.send_message("Found logs:")
            for msg in message:
                new_msg = msg.replace("`", "\`")
                await interaction.channel.send(f"```\n{new_msg}```")

    @commands.command(name="logs")
    async def classic_logs(self, ctx: commands.Context, number=10) -> None:
        message = await self.logs_impl(number)
        if type(message) == discord.Embed:
            await ctx.send(embed=message)
        else:
            for msg in message:
                new_msg = msg.replace("`", "\`")
                await ctx.send(f"```\n{new_msg}```")

    async def logs_impl(self, number=10) -> discord.Embed | str:
        try:
            with open(f"{TEMP_LOG_FILENAME}", "r") as f:
                lines = sum(1 for _ in f)
            with open(TEMP_LOG_FILENAME, "r") as f:
                if lines == 0:
                    embed = discord.Embed(
                        description="No Logs", color=0xFF0000
                    )
                    return embed
                if number > lines:
                    number = lines
                all_msg = ""
                for index, line in enumerate(f):
                    if lines - index <= number:
                        all_msg += f"{line}"
                final_msg = []
                last_occ = 0
                while (
                    len(all_msg[last_occ::]) > 0
                    and all_msg.rfind("\n", last_occ, last_occ + 1900) != -1
                ):
                    next_occ = all_msg.rfind("\n", last_occ, last_occ + 1900)
                    final_msg.append(all_msg[last_occ : next_occ + 1])
                    last_occ = next_occ + 1
                return final_msg
        except FileNotFoundError:
            embed = discord.Embed(description="No Logs", color=0xFF0000)
            return embed

    @classic_logs.error
    async def logs_error(self, ctx, error):
        if isinstance(error, MissingAnyRole):
            await ctx.send(
                f":no_entry_sign: **{ctx.message.author.name}**, you can't use that."
            )
        elif isinstance(error, UserNotFound):
            await ctx.send(embed=self.error_embed)
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(embed=self.error_embed)
        else:
            logging_error(error)

    @slash_logs.error
    async def slash_logs_error(self, interaction: Interaction, error):
        if isinstance(error, app_errors.MissingAnyRole):
            await interaction.response.send_message(
                content=f":no_entry_sign: **{interaction.user.name}**, you can't use that.",
                ephemeral=True,
            )
        else:
            logging_error(error)


async def setup(client):
    await client.add_cog(LogsCommand(client))
