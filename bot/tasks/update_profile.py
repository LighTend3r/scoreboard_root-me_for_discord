from discord.ext import commands, tasks
import datetime
from utils.db import Dabatase
from utils.api_rm import get_user_by_id, get_challenge_by_id
import time
import traceback
from utils.logging import info

class UpdateProfile(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.update_profile.start()

    # @tasks.loop(time=datetime.time(hour=4, minute=0, tzinfo=datetime.timezone.utc))
    @tasks.loop(hours=1)
    async def update_profile(self) -> None:
        try:
            info("Running need update tasks")

            cursor = Dabatase().get_cursor()

            # Update all users
            r = cursor.execute("SELECT * FROM user_rm")
            users = r.fetchall()

            for user in users:

                user_rm = get_user_by_id(user[1])
                info(f"[UPDATE] Mise à jour du profil de {user_rm['nom']}")

                if not user_rm:
                    continue

                cursor.execute("UPDATE user_rm SET score=?, rang=?, position=? WHERE id_auteur=?", (user_rm["score"], user_rm["rang"], user_rm["position"], user[1]))

                for chall in user_rm["validations"]:
                    data_validations = datetime.datetime.strptime(chall["date"], "%Y-%m-%d %H:%M:%S")

                    r = cursor.execute("SELECT COUNT(*) FROM solve WHERE id_auteur=? AND id_challenge=?", (user[1],chall["id_challenge"],))
                    challenge = r.fetchone()

                    if challenge[0] == 0:
                        info(f"[UPDATE] Ajout du challenge {chall['titre']} pour {user_rm['nom']}")
                        r = cursor.execute("SELECT * FROM solve WHERE id_challenge=?", (chall["id_challenge"],))
                        challenge_alread_here = r.fetchone()


                        if challenge_alread_here:
                            cursor.execute("INSERT INTO solve (id_auteur, id_challenge, titre, rubrique, score, id_rubrique, url_challenge, difficulte, timestamp) VALUES (?,?,?,?,?,?,?,?,?)", (
                                user[1],
                                challenge_alread_here[2],
                                challenge_alread_here[3],
                                challenge_alread_here[4],
                                challenge_alread_here[5],
                                challenge_alread_here[6],
                                challenge_alread_here[7],
                                challenge_alread_here[8],
                                data_validations.isoformat(),
                                )
                            )
                        else:
                            challenge_rm = get_challenge_by_id(chall["id_challenge"])
                            time.sleep(0.3)
                            cursor.execute("INSERT INTO solve (id_auteur, id_challenge, titre, rubrique, score, id_rubrique, url_challenge, difficulte, timestamp) VALUES (?,?,?,?,?,?,?,?,?)", (
                                user[1],
                                chall["id_challenge"],
                                challenge_rm["titre"],
                                challenge_rm["rubrique"],
                                challenge_rm["score"],
                                challenge_rm["id_rubrique"],
                                challenge_rm["url_challenge"],
                                challenge_rm["difficulte"],
                                data_validations.isoformat()
                                )
                            )

                cursor.connection.commit()
        except Exception as e:
            logging.error(e)

    @update_profile.error
    async def update_profile_error(self, error) -> None:
        logging.error("An error occured")

    @update_profile.before_loop
    async def wait_for_bot_ready(self) -> None:
        await self.client.wait_until_ready()


async def setup(client) -> None:
    await client.add_cog(UpdateProfile(client))
