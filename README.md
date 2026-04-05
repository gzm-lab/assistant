# 🎙️ Assistant Vocal — Notes & Rappels GitHub

Un assistant vocal qui écoute tes messages vocaux sur **Discord**, les transcrit, et crée automatiquement des **Issues GitHub** organisées comme notes, rappels et actions.

## 🧠 Comment ça marche

```
Message vocal Discord (OGG)
        ↓
  Téléchargement (lib.py)
        ↓
Transcription offline (Vosk + ffmpeg)
        ↓
Analyse NLP (CamemBERT — français)
        ↓
  Création Issue GitHub
  (titre, priorité, date)
        ↓
Confirmation sur Discord
```

## 🚀 Quick Start

### Prérequis

- Python 3.10+
- `ffmpeg` installé sur le système
- Un modèle Vosk français téléchargé dans `model/`
- Un token Discord (bot)
- Un token GitHub avec accès `repo`

### Installation

```bash
git clone https://github.com/gzm-lab/assistant.git
cd assistant

pip install discord.py vosk PyGithub transformers torch python-dotenv requests
```

Télécharge le modèle Vosk français :

```bash
# Modèle léger (40MB)
wget https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip
unzip vosk-model-small-fr-0.22.zip -d model/
```

### Configuration

Crée un fichier `.env` à la racine :

```env
DISCORD_TOKEN=ton_token_discord
GITHUB_TOKEN=ton_personal_access_token
GITHUB_REPO=gzm-lab/assistant
```

### Lancer le bot

```bash
python lib_discord.py
```

## 📂 Structure

```
assistant/
├── lib_discord.py      # Bot Discord — point d'entrée principal
├── speech_to_text.py   # Transcription vocale (Vosk + ffmpeg)
├── lib_github.py       # Création d'Issues GitHub (PyGithub)
├── lib_ai.py           # Analyse NLP (CamemBERT — extraction de phrases clés)
├── lib.py              # Utilitaire : téléchargement des messages vocaux
├── .github/
│   └── ISSUE_TEMPLATE/ # Templates : note, reminder, action
└── model/              # Modèle Vosk (à télécharger séparément, non versionné)
```

## 🏷️ Organisation des Issues

Les Issues créées sont taguées automatiquement selon le contenu du message vocal :

| Label | Description |
|---|---|
| `note` | Idée rapide ou mémo |
| `reminder` | Rappel ou événement |
| `action` | Tâche à faire |
| `priority:high` | Mention de "urgent" ou "haute priorité" |
| `priority:medium` | Priorité par défaut |
| `priority:low` | Mention de "basse priorité" |

Le titre de l'Issue est formaté comme `[TÂCHE] <première phrase du message>`.  
Si une date est détectée (`JJ/MM/AAAA`), elle est ajoutée au label.

## 🛠️ Stack technique

| Composant | Technologie |
|---|---|
| Bot Discord | `discord.py` |
| Transcription vocale | `Vosk` (offline, modèle français) + `ffmpeg` |
| Conversion audio | `ffmpeg` (OGG → WAV) |
| Analyse NLP | `CamemBERT` via HuggingFace Transformers |
| Gestion GitHub | `PyGithub` |
| Config | `python-dotenv` |

## ⚠️ Notes

- Le bot fonctionne **entièrement en local** — la transcription est offline (pas d'API externe pour l'audio).
- Le modèle CamemBERT est utilisé pour l'extraction de phrases clés (optionnel).
- Les messages vocaux sont supprimés localement après traitement.
