from discord import Interaction
from discord.app_commands import command, guilds
from discord.ext import commands
from utils.config import GUILD_ID
from discord import Embed


class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    async def classic_help(self, ctx: commands.Context) -> None:
        await ctx.send("pong")

    @command(name="help")
    @guilds(GUILD_ID)
    async def slash_help(self, interaction: Interaction):
        """Display the help message"""

        embed = Embed(title="==== Help ====", description="Here are the commands available\n<> : required\n[] : optional", color=0x00ff00)

        embed.add_field(name="`/ping`", value="Ping the bot", inline=False)

        embed.add_field(name="`/add_user <pseudo:str | rm_id:int>`", value="Ajouter un utilisateur à la BDD", inline=False)
        embed.add_field(name="`/remove_user <pseudo:str | rm_id:int>`", value="Supprimer un utilisateur de la BDD", inline=False)
        embed.add_field(name="`/profile <pseudo:str | rm_id:int>`", value="Affiche le profil d'un utilisateur", inline=False)
        embed.add_field(name="`/scoreboard [period:str = \"all\" | force_update:bool = False]`", value="Affiche le scoreboard des utilisateurs dans la BDD", inline=False)
        embed.add_field(name="`/who_solved <name_chall:str | challenge_id:int>`", value="Affiche les utilisateurs ayant résolu un challenge", inline=False)
        embed.add_field(name="`/chall <name:str>`", value="Affiche tous les chall qui comporte \"name\" dans leur nom", inline=False)
        embed.add_field(name="`/search_profile <pseudo:str>`", value="Recherche un utilisateur sur ROOT ME", inline=False)



        await interaction.response.send_message(embed=embed)


async def setup(client):
    await client.add_cog(HelpCommand(client))
