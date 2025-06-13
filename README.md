# Assistant Vocal Discord

Un bot Discord qui convertit les messages vocaux en texte en utilisant Vosk, une solution de reconnaissance vocale légère et rapide.

## Fonctionnalités

- Capture des messages vocaux sur Discord
- Conversion automatique de la parole en texte
- Utilisation de Vosk pour une transcription rapide et légère
- Support du français
- Parfait pour Raspberry Pi

## Prérequis

- Python 3.x
- Token Discord Bot
- Dossier `mp3/` pour le stockage temporaire des fichiers audio
- Connexion Internet pour le téléchargement initial du modèle Vosk

## Installation

1. Cloner le dépôt
2. Installer les dépendances :
```bash
pip install discord.py python-dotenv vosk
```
3. Créer un fichier `.env` avec votre token Discord :
```
TOKEN=votre_token_discord
```

## Utilisation

1. Lancer le bot :
```bash
python lib_discord.py
```
2. Envoyer un message vocal dans un canal Discord
3. Le bot répondra avec la transcription du message

## Structure du Projet

- `lib_discord.py` : Configuration et logique du bot Discord
- `speech_to_text.py` : Module de transcription vocale utilisant Vosk
- `lib.py` : Fonctions utilitaires 