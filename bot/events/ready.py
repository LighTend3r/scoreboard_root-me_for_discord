from discord.ext import commands
from utils.config import GUILD_ID
from utils.logging import info

class ReadyEvent(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        info('Le bot est connecté et prêt!')

        await self.client.tree.sync(guild=self.client.get_guild(GUILD_ID))
        await self.client.tree.sync()




async def setup(client):
    await client.add_cog(ReadyEvent(client))
