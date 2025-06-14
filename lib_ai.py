import torch
from transformers import AutoTokenizer, AutoModel
import json
from datetime import datetime
import re

class TextAnalyzer:
    def __init__(self):
        print("Initialisation du modèle...")
        # Utilisation d'un modèle de classification en français plus récent
        self.model_name = "camembert-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.model.eval()
        print("Modèle initialisé avec succès!")

    def _extract_key_phrases(self, text):
        # Tokenisation du texte
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        # Obtention des embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Utilisation de la dernière couche cachée
            last_hidden_state = outputs.last_hidden_state[0]
            
            # Calcul de l'importance des tokens
            token_importance = torch.norm(last_hidden_state, dim=1)
            
            # Sélection des tokens les plus importants
            _, indices = torch.topk(token_importance, k=min(5, len(token_importance)))
            
            # Conversion des indices en tokens
            tokens = self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
            selected_tokens = [tokens[i] for i in indices]
            
            # Construction de la phrase
            phrase = ' '.join(selected_tokens).replace('##', '')
            return phrase

    def process_text(self, text):
        try:
            # Extraction de la phrase clé
            title = self._extract_key_phrases(text)
            print(f"Texte d'entrée: {text}")
            print(f"Titre extrait: {title}")
            
            return {
                "success": True,
                "data": {
                    "title": title,
                    "description": text,
                    "due_date": None,
                    "labels": ["task"]
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de l'analyse du texte: {str(e)}"
            }

    def _is_redundant(self, title, description):
        """Vérifie si la description est redondante avec le titre."""
        title_words = set(title.lower().split())
        desc_words = set(description.lower().split())
        common_words = title_words.intersection(desc_words)
        return len(common_words) / len(title_words) > 0.5 if title_words else False 