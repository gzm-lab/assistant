import discord
import os
from dotenv import load_dotenv

import lib
import speech_to_text as stt

import datetime
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch

# Charger le processeur et le modèle
processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")

# Déplacer le modèle sur le CPU
device = torch.device("cpu")
model = model.to(device)

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
    if message.author.bot:
        return
    else: 
        if message.attachments:
            channel = discord.utils.get(message.guild.text_channels, id=message.channel.id)
            attachment = message.attachments[0]
            file_name = round(message.created_at.timestamp())
            lib.dl_vocal_msg(attachment.url,file_name)
            if channel:
                await channel.send("On traite ça boss")
            msg = stt.transcribe(processor,model,f"mp3/{file_name}.ogg")
            print(msg) 
            torch.cuda.empty_cache()
            if channel:
                await channel.send(f"J'ai compris : {msg}")
client.run(TOKEN)


