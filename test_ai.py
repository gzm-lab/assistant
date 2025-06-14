from lib_ai import TextAnalyzer

def test_title_generation():
    # Initialisation de l'analyseur
    analyzer = TextAnalyzer()
    
    # Texte de test
    test_text = "c'est l'anniversaire de brigitte chambre laisser de cherche un cadeau faut vraiment que j'arrive à trouver le cadeau parce que son anniversaire arrive vite c'est le trente juin"
    
    # Test de la génération
    result = analyzer.process_text(test_text)
    
    if result["success"]:
        print("\nRésultat de l'analyse :")
        print(f"Titre généré : {result['data']['title']}")
    else:
        print(f"Erreur : {result['error']}")

if __name__ == "__main__":
    test_title_generation() 