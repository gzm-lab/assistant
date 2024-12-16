import discord
import os
from dotenv import load_dotenv
import lib
import datetime


# Charge les variables d'environnement
load_dotenv()

TOKEN = os.getenv('TOKEN')
#GUILD_ID = int(os.getenv('GUILD_ID'))
#CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
intents = discord.Intents.default()
intents.messages = True  # Pour lire les messages
intents.guilds = True     # Pour accéder aux serveurs
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_message(message):
     if message.attachments:
        attachment = message.attachments[0]
        lib.dl_vocal_msg(attachment.url,round(message.created_at.timestamp()))        

client.run(TOKEN)