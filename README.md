# 🎙️ Voice Assistant — GitHub Notes & Reminders

A voice-activated assistant that listens to your **Discord** voice messages, transcribes them offline, and automatically creates organized **GitHub Issues** as notes, reminders, and action items.

## 🧠 How It Works

```
Discord voice message (OGG)
        ↓
  Download (lib.py)
        ↓
Offline transcription (Vosk + ffmpeg)
        ↓
  NLP Analysis (CamemBERT — French)
        ↓
  GitHub Issue created
  (title, priority, due date)
        ↓
Discord confirmation reply
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- `ffmpeg` installed on the system
- A Vosk French model downloaded into `model/`
- A Discord bot token
- A GitHub personal access token (scope: `repo`)

### Installation

```bash
git clone https://github.com/gzm-lab/assistant.git
cd assistant

pip install discord.py vosk PyGithub transformers torch python-dotenv requests
```

Download the Vosk French model:

```bash
# Lightweight model (~40MB)
wget https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip
unzip vosk-model-small-fr-0.22.zip -d model/
```

### Configuration

Create a `.env` file at the root:

```env
DISCORD_TOKEN=your_discord_bot_token
GITHUB_TOKEN=your_personal_access_token
GITHUB_REPO=gzm-lab/assistant
```

### Run the bot

```bash
python lib_discord.py
```

## 📂 Project Structure

```
assistant/
├── lib_discord.py      # Discord bot — main entry point
├── speech_to_text.py   # Voice transcription (Vosk + ffmpeg)
├── lib_github.py       # GitHub Issue creation (PyGithub)
├── lib_ai.py           # NLP analysis (CamemBERT — key phrase extraction)
├── lib.py              # Utility: voice message download
├── .github/
│   └── ISSUE_TEMPLATE/ # Templates: note, reminder, action
└── model/              # Vosk model (download separately, not versioned)
```

## 🏷️ Issue Organization

Created Issues are automatically tagged based on the voice message content:

| Label | Description |
|---|---|
| `note` | Quick idea or memo |
| `reminder` | Reminder or event |
| `action` | Task to complete |
| `priority:high` | Detected keywords: "urgent" / "high priority" |
| `priority:medium` | Default priority |
| `priority:low` | Detected keyword: "low priority" |

Issue titles are formatted as `[TASK] <first sentence of the message>`.
If a date is detected (`DD/MM/YYYY`), it is added as a label.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Discord bot | `discord.py` |
| Voice transcription | `Vosk` (offline, French model) + `ffmpeg` |
| Audio conversion | `ffmpeg` (OGG → WAV) |
| NLP analysis | `CamemBERT` via HuggingFace Transformers |
| GitHub integration | `PyGithub` |
| Configuration | `python-dotenv` |

## ⚠️ Notes

- The bot runs **entirely locally** — transcription is offline, no external audio API.
- CamemBERT is used for key phrase extraction (optional enhancement).
- Voice messages are deleted locally after processing.
