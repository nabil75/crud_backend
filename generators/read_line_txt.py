def lire_ligne(fichier, i):
    """
    Ouvre un fichier texte et retourne la ligne i (indexée à partir de 1).
    
    Args:
        fichier (str): Le chemin vers le fichier texte.
        i (int): Le numéro de la ligne à extraire (commence à 1).
        
    Returns:
        str: Le contenu de la ligne i, ou un message d'erreur si la ligne n'existe pas.
    """
    
    try:
        with open(fichier, mode="r", encoding="utf-8") as f:
            lignes = f.readlines()  # Lire toutes les lignes
            if 1 <= i <= len(lignes):  # Vérifier que i est dans les limites
                return lignes[i - 1].strip()  # Retourner la ligne sans les espaces inutiles
            else:
                return f"La ligne {i} n'existe pas dans le fichier."
    except FileNotFoundError:
        return f"Le fichier {fichier} est introuvable."
    except Exception as e:
        return f"Une erreur est survenue : {e}"

# Exemple d'utilisation
# chemin_fichier = "./generators/reponses_esprit_competition.txt"
# ligne_voulue = lire_ligne(chemin_fichier, 5)
# print(ligne_voulue)