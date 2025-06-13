import json
from vosk import Model, KaldiRecognizer
import wave
import os
import subprocess

def init_model():
    # On suppose que le modèle est déjà dans le dossier 'model/'
    return Model("model")

model = None

def transcribe(processor, model_param, audio_path):
    global model
    try:
        if model is None:
            model = init_model()
        
        # Convertir le fichier audio en WAV
        wav_path = audio_path.replace('.ogg', '.wav')
        subprocess.run(['ffmpeg', '-i', audio_path, wav_path], check=True)
        
        wf = wave.open(wav_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Format audio non supporté. Conversion nécessaire.")
            return "Erreur: Format audio non supporté"
        
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part = json.loads(rec.Result())
                results.append(part.get("text", ""))
        part = json.loads(rec.FinalResult())
        results.append(part.get("text", ""))
        wf.close()
        os.remove(wav_path)  # Supprimer le fichier WAV temporaire
        os.remove(audio_path)  # Supprimer le fichier OGG original
        print(f"Fichiers audio supprimés : {wav_path} et {audio_path}")
        return " ".join(results)
    except Exception as e:
        msg = f"Erreur lors de la transcription : {e}"
        return msg
