from transformers import WhisperProcessor, WhisperForConditionalGeneration, EncoderDecoderCache
import torch
import torchaudio

# Chemin vers le fichier audio
def transcribe(processor,model,audio_path):
    try:
        # Charger l'audio
        speech_array, sampling_rate = torchaudio.load(audio_path)

        # Vérifier et ajuster le taux d'échantillonnage
        if sampling_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sampling_rate, new_freq=16000)
            speech_array = resampler(speech_array)

        # Préparer les entrées pour la transcription
        inputs = processor(
            speech_array.squeeze().numpy(),
            sampling_rate=16000,
            return_tensors="pt",
            language="fr",  # Langue française spécifiée
            task="transcribe",  # Transcription uniquement
            return_attention_mask=True
        )

        # Initialiser le cache de l'encodeur/décodeur
        encoder_decoder_cache = EncoderDecoderCache.from_legacy_cache(None)

        # Générer la transcription avec le cache
        with torch.no_grad():
            predicted_ids = model.generate(
                inputs["input_features"],
                attention_mask=inputs.get("attention_mask"),
                max_length=100,  # Limite la longueur des tokens générés
                num_beams=1,  # Simplifie la recherche
                no_repeat_ngram_size=2,  # Évite les répétitions
                past_key_values=encoder_decoder_cache  # Corrige le warning
            )

        # Décoder la transcription
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        
        return(transcription)

    except Exception as e:
        msg = f"Erreur lors de la transcription : {e}"
        return(msg)
