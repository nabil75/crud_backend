import pandas as pd
import matplotlib.pyplot as plt

# Fonction pour splitter les labels sur plusieurs lignes
def split_label(label, threshold):
    words = label.split()  # Diviser la chaîne en mots
    lines = []
    current_line = []

    # Construire les lignes sans dépasser le seuil par ligne
    for word in words:
        # Si ajouter le mot dépasse le seuil, on commence une nouvelle ligne
        if sum(len(w) for w in current_line) + len(current_line) + len(word) > threshold:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    
    # Ajouter la dernière ligne
    if current_line:
        lines.append(" ".join(current_line))
    
    # Retourner le label splitté avec des sauts de ligne
    return "\n".join(lines)

# Étape 1 : Créer un DataFrame avec vos données
data = {
    # 'Objet': ['Objet 1', 'Objet 2', 'Objet 3'],
    'semantique1': [3, 30, 71, 6, 32, 7, 24, 37, 71, 51, 66, 30, 22, 87, 70, 62, 66, 42, 34, 13],
    'semantique2': [56, 82, 38, 39, 76, 4, 84, 3, 25, 90, 85, 73, 41, 19, 51, 14, 59, 9, 99, 11],
    'semantique3': [94, 25, 28, 94, 15, 59, 22, 55, 39, 57, 13, 48, 49, 71, 71, 67, 16, 56, 77, 88],
    'semantique4': [81, 13, 10, 19, 53, 40, 19, 52, 56, 54, 54, 1, 49, 65, 14, 22, 14, 29, 46, 26]
}

df = pd.DataFrame(data)

# Étape 2 : Calculer la moyenne pour chaque dimension sémantique
moyennes = {
    "Elle permet de souder le couple": df['semantique1'],
    "C'est un moment de calme": df['semantique2'],
    "C'est un pur bonheur": df['semantique3'],
    "C'est une activité très stimulante pour la créativité":df['semantique4']
}

# Calculer les moyennes globales
moyennes_df = pd.DataFrame(moyennes).mean()
new_labels = [split_label(label, 15) for label in moyennes_df.index]

# Étape 3 : Créer le graphique en inversant les axes
fig, ax1 = plt.subplots(figsize=(4, 4))

# Tracer les points et les relier avec une ligne sur le premier axe y
ax1.plot(moyennes_df.values, new_labels, marker='o', linestyle='-', color='blue')
# Ajouter une ligne verticale pour la valeur 0
ax1.axvline(0, color='black', linewidth=1, linestyle='-')
ax1.set_xlim(0, 100)  # Ajuster l'échelle des évaluations
ax1.grid(True, axis='x')  # Grille seulement sur l'axe des x

# Ajuster les marges pour rendre le graphique plus compact
plt.subplots_adjust(left=0.2, right=0.8)

# Étape 5 : Ajouter un deuxième axe y
ax2 = ax1.twinx()  # Créer un second axe y

# Par exemple, ajoutons des données fictives pour le deuxième axe
# Remplacez ces valeurs par les données réelles que vous souhaitez afficher

deuxieme_axe_donnees = {
    "C'est une source de discorde": df['semantique1'],
    "C'est un moment d'exitation": df['semantique2'],
    "C'est un vrai calvaire": df['semantique3'],
    "C'est une activité rébarbative":df['semantique4']
} 

deuxieme_axe_donnees_df = pd.DataFrame(deuxieme_axe_donnees).mean()
new_labels2 = [split_label(label, 15) for label in deuxieme_axe_donnees_df .index]
# Données fictives
ax2.plot( deuxieme_axe_donnees_df.values, new_labels2, marker='o', linestyle='-', color='blue')

#Personnaliser le deuxième axe y
# ax2.set_ylabel("Deuxième axe y (données fictives)")
# ax2.set_ylim(-3, 3)  # Ajuster l'échelle du deuxième axe y

# Afficher le graphique
plt.show()

# Sauvegarder l'image dans un buffer BytesIO
buf = io.BytesIO()
fig.savefig(buf, format='png', transparent=True)
buf.seek(0)

# Retourner l'image comme réponse
return StreamingResponse(buf, media_type='image/png')

