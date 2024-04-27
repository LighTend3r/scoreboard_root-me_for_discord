from discord import Interaction
from discord.app_commands import command, guilds
from discord.ext import commands
from utils.config import GUILD_ID
from utils.api_rm import get_all_chall_by_name
from discord import Embed
import traceback

dict_category = {
    "189": "App-Script",
    "203": "App-Systeme",
    "69": "Cracking",
    "18": "Cryptanalyse",
    "208": "Forensic",
    "17": "Programmation",
    "70": "Realiste",
    "182": "Reseau",
    "67": "Steganographie",
    "16": "Web-Client",
    "68": "Web-Serveur",
}

class ChallCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @command(name="chall")
    @guilds(GUILD_ID)
    async def slash_chall(self, interaction: Interaction, name:str):
        """Display all challenges including the name provided"""

        await interaction.response.defer()

        all_challenges = get_all_chall_by_name(name)

        print(all_challenges)
        print(all_challenges.keys())

        message_to_display = ""
        for chall in list(all_challenges.keys())[:10]:
            chall = all_challenges[chall]
            message_to_display += f"(id : {chall['id_challenge']}) **{chall['titre']}** - {dict_category[chall['id_rubrique']]}\n"

        embed = Embed(title="==== Challenges ====", description=message_to_display, color=0x00ff00)
        await interaction.followup.send(embed=embed)

    @slash_chall.error
    async def slash_error(self, interaction: Interaction, error):
        print(traceback.format_exc())
        await interaction.followup.send("An error occured")

async def setup(client):
    await client.add_cog(ChallCommand(client))
