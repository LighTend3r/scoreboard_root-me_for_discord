from discord import Interaction
from discord.app_commands import command, guilds, Choice, choices
from discord.ext import commands
from utils.config import GUILD_ID
from utils.api_rm import get_user_by_id
from utils.db import Dabatase
from discord import Embed
from datetime import datetime, timedelta
from utils.logging import error as logging_error

def place_to_str(place):
    if place == 1:
        return ":first_place:"
    elif place == 2:
        return ":second_place:"
    elif place == 3:
        return ":third_place:"
    else:
        return f"{place}th"

class ScoreboardCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @command(name="scoreboard")
    @guilds(GUILD_ID)
    @choices(
        period=[
            Choice(name="last one day", value=1),
            Choice(name="last week", value=7),
            Choice(name="last month", value=30),
            Choice(name="last year", value=365),
            Choice(name="all", value=999),
        ]
    )
    async def slash_scoreboard(self, interaction: Interaction, period: int=999, force_update:bool = False):
        """Display the scoreboard"""

        await interaction.response.defer()

        cursor = Dabatase().get_cursor()

        if force_update:
            # Update all users
            r = cursor.execute("SELECT * FROM user_rm")
            users = r.fetchall()
            for user in users:
                user_rm = get_user_by_id(user[1])
                if not user_rm:
                    continue
                cursor.execute("UPDATE user_rm SET score=?, rang=?, position=? WHERE id_auteur=?", (user_rm["score"], user_rm["rang"], user_rm["position"], user[1]))

        today = datetime.now()
        if period == 999:
            r = cursor.execute("SELECT * FROM user_rm ORDER BY score DESC")
            users = r.fetchall()


            message_to_display = ""
            for i, user in enumerate(users):
                message_to_display += f"{place_to_str(i + 1)} **{user[2]}**: Score: {user[3]}\n"

            embed = Embed(title="==== Scoreboard ====", description=message_to_display, color=0x00ff00)

            await interaction.followup.send(embed=embed)
        else:
            first_date = today - timedelta(days=period)
            first_date = first_date.isoformat()
            r = cursor.execute("SELECT u.id_auteur,u.nom,SUM(s.score) as score FROM user_rm u JOIN solve s ON u.id_auteur=s.id_auteur HAVING s.timestamp > ? GROUP BY u.id_auteur,u.nom ORDER BY score DESC", (first_date,))

            users = r.fetchall()

            message_to_display = ""
            for i, user in enumerate(users):
                message_to_display += f"{place_to_str(i + 1)} **{user[1]}**: Score: {user[2]}\n"

            if len(users) == 0:
                message_to_display = "No user found"

            embed = Embed(title=f"==== Scoreboard for the last {period} days ====", description=message_to_display, color=0x00ff00)

            await interaction.followup.send(embed=embed)




    @slash_scoreboard.error
    async def slash_error(self, interaction: Interaction, error):
        await interaction.followup.send("An error occured")
        logging_error(error)

async def setup(client):
    await client.add_cog(ScoreboardCommand(client))
