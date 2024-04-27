from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
RM_API_TOKEN = os.getenv('RM_API_TOKEN')
