from discord import Interaction
from discord.app_commands import command, guilds
from discord.ext import commands
from utils.config import GUILD_ID
from utils.db import Dabatase
from discord import Embed
import traceback
from utils.api_rm import get_all_chall_by_name
from utils.logging import error as logging_error

class WhoSolvedCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @command(name="who_solved")
    @guilds(GUILD_ID)
    async def slash_who_solved(self, interaction: Interaction, name_chall:str = "", challenge_id: int= 0):
        """Display all users who solved the challenge provided"""

        await interaction.response.defer()

        if challenge_id == 0 and name_chall == "":
            await interaction.followup.send("You need to provide a challenge id or a challenge name")
            return

        if name_chall != "":
            all_challenges_rm = await get_all_chall_by_name(name_chall)

            if not all_challenges_rm or len(all_challenges_rm) == 0:
                await interaction.followup.send("Challenge not found")
                return

            if len(all_challenges_rm) > 1:
                message_to_display = ""
                for chall in list(all_challenges_rm.keys())[:10]:
                    chall = all_challenges_rm[chall]
                    message_to_display += f"(id : {chall['id_challenge']}) **{chall['titre']}**\n"

                embed = Embed(title="==== Found ====", description=message_to_display, color=0x00ff00)
                await interaction.followup.send("Too many challenges found", embed=embed)
                return

            challenge_id = all_challenges_rm["0"]["id_challenge"]

        cursor = Dabatase().get_cursor()

        r = cursor.execute("SELECT * FROM solve WHERE id_challenge=? ORDER BY score DESC", (challenge_id,))
        users = r.fetchall()

        if not users:
            await interaction.followup.send("No user solved this challenge (or is not challenge id)")
            return

        nom_challenge = users[0][3]

        message_to_display = ""
        for user in users[:25]:
            r = cursor.execute("SELECT nom FROM user_rm WHERE id_auteur=?", (user[1],))
            nom = r.fetchone()
            message_to_display += f"{nom[0]}\n"

        embed = Embed(title=nom_challenge, color=0x00ff00)
        embed.add_field(name="Solved by", value=message_to_display)
        await interaction.followup.send(embed=embed)


    @slash_who_solved.error
    async def slash_error(self, interaction: Interaction, error):
        await interaction.followup.send("An error occured")
        logging_error(error)

async def setup(client):
    await client.add_cog(WhoSolvedCommand(client))
