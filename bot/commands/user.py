from discord import Interaction
from discord.app_commands import command, guilds
from discord.ext import commands
from utils.config import GUILD_ID
from utils.api_rm import get_user_by_id, get_all_users_by_name
from utils.db import Dabatase
from datetime import datetime
from discord import Embed
from discord.app_commands import Choice
from typing import List
import traceback
from utils.logging import error as logging_error


class UserCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @command(name="add_user")
    @guilds(GUILD_ID)
    async def slash_add_user(self, interaction: Interaction, pseudo:str = "", rm_id:int=0):
        """Add user in database"""

        await interaction.response.defer()

        if pseudo== "" and rm_id == 0:
            await interaction.followup.send("You need to provide a user")
            return

        if pseudo != "":
            all_user_rm = await get_all_users_by_name(pseudo)

            if not all_user_rm or len(all_user_rm) == 0:
                await interaction.followup.send("User not found")
                return

            if len(all_user_rm) > 1:
                message_to_display = ""
                for user in list(all_user_rm.keys())[:10]:
                    user = all_user_rm[user]
                    message_to_display += f"(id : {user['id_auteur']}) **{user['nom']}**\n"

                embed = Embed(title="==== Found ====", description=message_to_display, color=0x00ff00)
                await interaction.followup.send("Too many users found", embed=embed)
                return
            rm_id = all_user_rm["0"]["id_auteur"]

        cursor = Dabatase().get_cursor()

        r = cursor.execute("SELECT * FROM user_rm WHERE id_auteur=?", (rm_id,))
        user = r.fetchone()
        if user:
            await interaction.followup.send("User already in database")
            return


        user = await get_user_by_id(rm_id)
        if not user:
            await interaction.followup.send("User not found")
            return

        now = datetime.now().isoformat()

        cursor.execute("INSERT INTO user_rm (id_auteur, nom, score, rang, position, timestamp) VALUES (?,?,?,?,?,?)", (user["id_auteur"], user["nom"], user["score"], user["rang"], user["position"], now))
        cursor.connection.commit()

        await interaction.followup.send(f"User {user['nom']} added")

    @command(name="remove_user")
    @guilds(GUILD_ID)
    async def slash_remove_user(self, interaction: Interaction, pseudo:str = "", rm_id:int=0):
        """Remove user in database"""

        await interaction.response.defer()

        if pseudo == "" and not rm_id:
            await interaction.followup.send("You need to provide a user")
            return


        try:
            if pseudo != "":
                cursor = Dabatase().get_cursor()
                r = cursor.execute("SELECT * FROM user_rm WHERE nom=?", (pseudo,))
                user = r.fetchone()

                rm_id = user[1]

            else:
                cursor = Dabatase().get_cursor()
                r = cursor.execute("SELECT * FROM user_rm WHERE id_auteur=?", (rm_id,))
                user = r.fetchone()

        except Exception:
            await interaction.followup.send("User not found")
            return

        cursor = Dabatase().get_cursor()

        r = cursor.execute("SELECT nom FROM user_rm WHERE id_auteur=?", (rm_id,))
        nom = r.fetchone()

        if not nom:
            await interaction.followup.send("User not found")
            return

        cursor.execute("DELETE FROM user_rm WHERE id_auteur=?", (rm_id,))
        cursor.execute("DELETE FROM solve WHERE id_auteur=?", (rm_id,))

        cursor.connection.commit()

        await interaction.followup.send(f"User {nom[0]} removed")

    @command(name="profile")
    @guilds(GUILD_ID)
    async def slash_profile(self, interaction: Interaction, pseudo:str = "", rm_id:int = 0):
        """Get user profile"""

        await interaction.response.defer()

        if pseudo == "" and not rm_id:
            await interaction.followup.send("You need to provide a user")
            return


        try:
            if pseudo != "":
                cursor = Dabatase().get_cursor()
                r = cursor.execute("SELECT * FROM user_rm WHERE nom=?", (pseudo,))
                user = r.fetchone()

                rm_id = user[1]
                added_at = user[6]

            else:
                cursor = Dabatase().get_cursor()
                r = cursor.execute("SELECT * FROM user_rm WHERE id_auteur=?", (rm_id,))
                user = r.fetchone()

                added_at = user[6]
        except Exception:
            await interaction.followup.send("User not found")
            return

        user_rm = await get_user_by_id(rm_id)

        if not user:
            await interaction.followup.send("User not found")
            return

        cursor.execute("UPDATE user_rm SET score=?,position=?,rang=? WHERE nom=? and id_auteur=?", (user_rm['score'],user_rm['position'],user_rm['rang'],pseudo,user_rm['id_auteur']))
        cursor.connection.commit()

        embed = Embed(
            title=f"Profile of {user_rm['nom']}",
            description=f"Id: {user_rm['id_auteur']}",
            color=0x00ff00
        )
        embed.add_field(name="Score", value=user_rm['score'], inline=True)
        embed.add_field(name="Position", value=user_rm['position'], inline=True)
        embed.add_field(name="Rank", value=user_rm['rang'], inline=True)

        added_at = datetime.fromisoformat(added_at)

        embed.set_footer(text="Added at " + added_at.strftime("%d/%m/%Y %H:%M:%S"))

        await interaction.followup.send(embed=embed)

    @slash_remove_user.autocomplete("pseudo")
    @slash_profile.autocomplete("pseudo")
    async def parameters_autocomplete(
        self, interaction: Interaction, current: str
    ) -> List[Choice[str]]:
        try:
            # On lance la recherche à partir de 3 caractères
            if len(current) < 3:
                return []

            parameters_found = []

            cursor = Dabatase().get_cursor()

            r = cursor.execute("SELECT nom FROM user_rm WHERE nom LIKE ?", (f"%{current}%",))
            users = r.fetchall()

            for user in users:
                parameters_found.append(user[0])

            return [
                Choice(value=name, name=name)
                for (name) in parameters_found[0 : min(25, len(parameters_found))]
            ]

        except Exception as e:
            logging.error(e)
            return []


    @slash_add_user.error
    @slash_remove_user.error
    @slash_profile.error
    async def slash_add_user_error(self, interaction: Interaction, error):
        await interaction.followup.send("An error occured")
        logging_error(error)

async def setup(client):
    await client.add_cog(UserCommand(client))
