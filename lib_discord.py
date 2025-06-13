import discord
import os
from dotenv import load_dotenv
import lib
import speech_to_text as stt
from lib_github import GitHubManager

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

# Initialisation des services
print("Initialisation du modèle Vosk...")
stt.init_model()
print("Modèle Vosk initialisé !")

print("Initialisation de GitHub...")
github_manager = GitHubManager()
print("GitHub initialisé !")

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
            
            # Téléchargement et traitement du message vocal
            if lib.dl_vocal_msg(attachment.url, file_name):
                if channel:
                    await channel.send("On traite ça boss")
                
                # Transcription du message vocal
                transcribed_text = stt.transcribe(None, None, f"mp3/{file_name}.ogg")
                print(f"Texte transcrit : {transcribed_text}")
                
                if channel:
                    await channel.send(f"J'ai compris : {transcribed_text}")
                
                # Création de l'issue GitHub
                result = github_manager.create_issue(transcribed_text)
                if result['success']:
                    await channel.send(f"✅ Tâche créée ! Issue #{result['issue_number']} : {result['issue_url']}")
                else:
                    await channel.send(f"❌ Erreur lors de la création de la tâche : {result['error']}")
            else:
                if channel:
                    await channel.send("❌ Erreur lors du téléchargement du message vocal")

client.run(TOKEN)


