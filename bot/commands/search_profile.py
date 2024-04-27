from discord import Interaction
from discord.app_commands import command, guilds
from discord.ext import commands
from utils.config import GUILD_ID
from utils.api_rm import get_all_users_by_name
import traceback


class SearchProfileCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @command(name="search_profile")
    @guilds(GUILD_ID)
    async def slash_search_profile(self, interaction: Interaction, pseudo:str):
        """Search profile on root-me api"""

        await interaction.response.defer()

        all_users_rm = get_all_users_by_name(pseudo)

        if not all_users_rm:
            await interaction.followup.send("User not found")
            return

        message_to_display = ""
        for user in list(all_users_rm.keys())[:25]:
            user = all_users_rm[user]
            message_to_display += f"{user['nom']} (id:{user['id_auteur']})\n"

        await interaction.followup.send(message_to_display)



    @slash_search_profile.error
    async def slash_add_user_error(self, interaction: Interaction, error):
        print(traceback.format_exc())
        await interaction.followup.send("An error occured")

async def setup(client):
    await client.add_cog(SearchProfileCommand(client))
