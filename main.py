import base64
from email import message
import io
import logging
from pyexpat.errors import messages
import string
from fastapi import FastAPI, params
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import *
from archive.llmstudio import *
from generative_chatgpt import auto_generate_contexte, auto_generate_questionnaire, auto_generate_themes
from third_party_functions import *
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
from langdetect import detect
from openai import OpenAI

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:4200",  # Angular frontend
    # Add more origins as needed, e.g., "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


                                                        # # # # # # # # # # # # # # # # # # #
                                                        #                                   #  
                                                        #   Opérations sur Questionnaire    #
                                                        #                                   #
                                                        # # # # # # # # # # # # # # # # # # #

@app.get("/all_questionnaries")
async def all_questionnaries():
    obj = []
    query="select id_questionnary, content_questionnary from questionnary"
    records = await postgres_select_query(query)
    id_questionnaries = [record["id_questionnary"] for record in records]
    parsed_id_questionnaries = [json.loads(str(id)) for id in id_questionnaries]
    cleaned_content_records = [record["content_questionnary"] for record in records]
    parsed_content_records = [json.loads(content) for content in cleaned_content_records]
    obj = [{"position":parsed_id_questionnaries[parsed_content_records.index(content_record)], "intitule":content_record[0]['intitule'] ,"date":content_record[0]['date'], 
    "nombre_questions":len(content_record[0]['questions'])} for content_record in parsed_content_records]
    return  obj

@app.get("/get_questionnary/{idQuestionnary}")
async def get_questionnary(idQuestionnary:int):
    obj = []
    query = "select id_questionnary, content_questionnary from questionnary where id_questionnary = $1"
    params = (idQuestionnary)
    records = await postgres_select_query(query, params)
    cleaned_content_records = [record["content_questionnary"] for record in records]
    parsed_content_records = [json.loads(content) for content in cleaned_content_records]
    obj = [{"position":idQuestionnary, "intitule":content_record[0]['intitule'] ,"date":content_record[0]['date'], 
    "content":content_record[0]['questions']} for content_record in parsed_content_records]
    return obj

@app.get("/save_questionnary/{content}")
async def save_questionnary (content):
    query = "INSERT INTO questionnary (content_questionnary) VALUES ($1) RETURNING id_questionnary"
    params = (content)
    last_id = await postgres_insert_query(query, params)
    return (last_id)

@app.get("/update_questionnary/{idQuestionnary}/{content}")
async def update_questionnary (idQuestionnary:int,  content):
    query = "UPDATE questionnary SET content_questionnary = $1 WHERE id_questionnary = $2"
    params = (content, idQuestionnary)
    await postgres_update_query(query, *params)
    return "Questionnaire modifié"

@app.get("/delete_questionnary/{idQuestionnary}")
async def delete_questionnary (idQuestionnary:int):
    query = "DELETE FROM questionnary WHERE id_questionnary = $1"
    params = (idQuestionnary)
    await postgres_delete_query(query, params)
    return "Questionnaire supprimé"

@app.get("/get_auto_questionnary/{role}/{objet_comprendre}/{objet_mesurer}/{finalite}/{selectedThemes}/{modelSelected}")
async def get_auto_questionnary(role, objet_comprendre, objet_mesurer, finalite, selectedThemes, modelSelected):
    return await auto_generate_questionnaire(role, objet_comprendre, objet_mesurer, finalite, selectedThemes, modelSelected)

@app.get("/get_auto_themes/{role}/{objet_comprendre}/{objet_mesurer}/{finalite}/{modelSelected}")
async def get_auto_themes(role, objet_comprendre, objet_mesurer, finalite, modelSelected):
    return await auto_generate_themes(role, objet_comprendre, objet_mesurer, finalite, modelSelected)

@app.get("/get_auto_contexte/{theme_contexte}/{modelSelected}")
async def get_auto_contexte(theme_contexte, modelSelected):
    return await auto_generate_contexte(theme_contexte, modelSelected)

@app.get("/save_auto_proposition/{cadre_etude}/{role}/{objectif_comprendre}/{objectif_mesurer}/{finalite}/{themes}")
async def save_auto_proposition(cadre_etude, role, objectif_comprendre, objectif_mesurer, finalite, themes):
    themes = json.dumps(themes)
    query = "INSERT INTO auto_proposition (cadre_etude, role, objectif_comprendre, objectif_mesurer, finalite, themes) VALUES ($1,$2,$3,$4,$5,$6) RETURNING id_proposition"
    last_id = await postgres_insert_query(query, cadre_etude, role, objectif_comprendre, objectif_mesurer, finalite, themes)
    return (last_id)
    
                                                        # # # # # # # # # # # # # # # # # # #
                                                        #                                   #  
                                                        #       Résultats questions         #
                                                        #                                   #
                                                        # # # # # # # # # # # # # # # # # # #


@app.get("/get_results_fermee/{idQuestionnary}/{idQuestion}")
async def get_results_fermee(idQuestionnary:int, idQuestion:int):
    data=[]
    valeurs=[]
    query = "SELECT * from results where id_questionnary = $1 ORDER BY id_result ASC"
    params = (idQuestionnary)
    records = await postgres_select_query(query, params)
    content = json.loads(records[0]['content_result'])
    #Récupérer les libellés des modalités
    list_labels = [modality['libelle'] for modality in content[0]['questions'][idQuestion]['modalites']]

    # #Comptage du nombre de valeurs 'true' pour chaque modalité
    val_tot=[]
    for record in records:
        content = json.loads(record[1])
        reponses =content[0]['questions'][idQuestion]['modalites']
        val=[]
        for reponse in reponses:
            if (reponse['isChecked'] == True):
                val.append(1)
            else:
                val.append(0)
        val_tot.append(val)
    data=sumReponseTrue(val_tot)

    return {"labels":list_labels, "values":data}



@app.get("/get_results_echelle/{idQuestionnary}/{idQuestion}")
async def get_results_echelle(idQuestionnary:int, idQuestion:int):
    data={}
    semantique_gauche=[]
    semantique_droit=[]
    query = "SELECT * from results where id_questionnary = $1"
    params = (idQuestionnary)
    records = await postgres_select_query(query, params)
    #Récupérer les libellés des modalités
    content = json.loads(records[0][1])
    reps =content[0]['questions'][idQuestion]['semantiques']
    for rep in reps:
        semantique_gauche.append(rep['libelleGauche'])
        semantique_droit.append(rep['libelleDroit'])
        list_semantique_gauche = json.loads(json.dumps(semantique_gauche))
        list_semantique_droit = json.loads(json.dumps(semantique_droit))
    #Comptage du nombre de valeurs 'true' pour chaque modalité

    nb_semantiques = len(list_semantique_droit)
    j=0
    for i in range(nb_semantiques):
        data_semantique=[]
        for record in records:
            content = json.loads(record[1])
            reponse =content[0]['questions'][idQuestion]['semantiques'][i]
            data_semantique.append(int(reponse['valeur']))
        data[str(j)]=data_semantique
        j+=1
    return {"semantiqueGauche":list_semantique_gauche, "semantiqueDroite":list_semantique_droit, "data":data}

@app.get("/get_results_notation/{idQuestionnary}/{idQuestion}")
async def get_results_notation(idQuestionnary:int, idQuestion:int):
    notes_occurences=""
    notes=[]
    query = "SELECT * from results where id_questionnary = $1"
    params = (idQuestionnary)
    records = await postgres_select_query(query, params)
    for record in records:
        content = json.loads(record[1])
        reponses =content[0]['questions'][idQuestion]['note']
        notes.append(reponses)

    query_stars = "SELECT * from questionnary where id_questionnary = $1"
    params_stars = (idQuestionnary)
    records = await postgres_select_query(query_stars, params_stars)
    for record in records:
        content = json.loads(record[1])
        max_stars =content[0]['questions'][idQuestion]['nbStars']

    #Comptage du nombre de valeurs pour chaque liveau d'étoiles
    notes_occurences =  count_occurrences(notes, max_stars)
    return notes_occurences

@app.get("/get_results_satisfaction/{idQuestionnary}/{idQuestion}")
async def get_results_satisfaction(idQuestionnary:int, idQuestion:int):
    notes_occurrences=""
    notes=[]
    query = "SELECT * from results where id_questionnary = $1"
    params = (idQuestionnary)
    records = await postgres_select_query(query, params)
    for record in records:
        content = json.loads(record[1])
        reponse =content[0]['questions'][idQuestion]['note']
        notes.append(int(reponse))


    query_stars = "SELECT * from questionnary where id_questionnary = $1"
    params_stars = (idQuestionnary)
    records = await postgres_select_query(query_stars, params_stars)
    for record in records:
        content = json.loads(record[1])
        satisfaction_levels =content[0]['questions'][idQuestion]['echelle_list']

    levels = len(satisfaction_levels)
    #Comptage du nombre de valeurs pour chaque liveau d'étoiles
    notes_occurrences =  count_occurrences(notes, levels)
    return {"occurrences":notes_occurrences, "niveaux":satisfaction_levels}

@app.get("/get_results_grille/{idQuestionnary}/{idQuestion}")
async def get_results_grille(idQuestionnary: int, idQuestion: int):
    notes_occurrences = ""
    reponses = []

    query = "SELECT * from results where id_questionnary = $1"
    params = (idQuestionnary)
    records = await postgres_select_query(query, params)
    for record in records:
        content = json.loads(record[1])
        reps = content[0]['questions'][idQuestion]['lignes']
        arr_rep = []
        for rep in reps:
            arr_rep.append(rep['reponse'])
        reponses.append(arr_rep)

    query = "SELECT * from questionnary where id_questionnary = $1"
    params = (idQuestionnary)
    records = await postgres_select_query(query, params)
    content = json.loads(records[0][1])
    reps = content[0]['questions'][idQuestion]['colonnes']
    levels = [rep['libelle'] for rep in reps]

    reps = content[0]['questions'][idQuestion]['lignes']
    items = [rep['libelle'] for rep in reps]

    results = [[0] * len(levels) for _ in range(len(items))]


    # Vérification de la taille des réponses
    if any(len(responses) > len(results) for responses in reponses):
        print("Unexpected response size, skipping processing for some entries.")

    # Parcours des réponses de chaque individu
    for responses in reponses:
        for i, response in enumerate(responses):
            if i >= len(results):
                print(f"Skipping response at index {i} because it's out of range for results.")
                continue
            if isinstance(response, int) and 1 <= response <= len(levels):
                results[i][response - 1] += 1
            else:
                print(f"Skipping invalid response value: {response}, expected an integer between 1 and {len(levels)}")

    return {"data": results, "levels": levels, "items": items}


@app.get("/get_libelle_question")
async def get_libelle_question_from_llmstudio():
    libelle =""
    libelle = get_libelle_question()
    return libelle

@app.get("/insert_result/{content}/{idQuestionnary}")
async def save_questionnary (content, idQuestionnary:int):
    query = "INSERT INTO results (content_result, id_questionnary) VALUES ($1, $2) RETURNING id_result"
    params = (content, idQuestionnary)
    last_id = await postgres_insert_query(query, *params)
    return (last_id)

                                                        # # # # # # # # # # # # # # # # # # #
                                                        #                                   #  
                                                        #           Graphiques              #
                                                        #                                   #
                                                        # # # # # # # # # # # # # # # # # # #

@app.get("/plot_bar/{data}/{theme}/{type_tableau}")
async def get_plot_bar(data, theme, type_tableau):
    json_data = json.loads(data)
    color_chart ="white" if theme =="dark" else "black"
    fig, ax = plt.subplots()
     # Convert each value to a percentage or frequencies depending on type_tableau value (true or false)
    
    if (type_tableau == "false"):
        percentage_data = [(value / sum(json_data['values'])) * 100 for value in json_data['values']] # Convert each value to a percentage
        percentage_data = [round(value, 2) for value in percentage_data] # Round each value to 2 decimal places
        ax.bar(json_data['labels'],  percentage_data)
        # Add value labels on top of each bar
        for i, value in enumerate(percentage_data):
            plt.text(i, value + 0.5, str(value), ha='center', va='bottom', color=color_chart, fontsize=10)
    else:
        ax.bar(json_data['labels'],  json_data['values'])
        for i, value in enumerate(json_data['values']):
                plt.text(i, value + 0.5, str(value), ha='center', va='bottom', color=color_chart, fontsize=10)


    nb_labels = len(json_data['labels'])
   
    # Seuil pour scinder les labels sur deux lignes
    if(nb_labels>5):
        new_labels = [split_label(label, 20) for label in json_data['labels']]
        ax.set_xticklabels(new_labels, ha='right', rotation=45)
    else:
        match nb_labels:
            case value if value <3:
                threshold = 20
            case value if value <5:
                threshold = 15
            case _:
                threshold = 10
        
        # Appliquer la fonction de split sur tous les labels
        new_labels = [split_label(label, threshold) for label in json_data['labels']]
        # Appliquer les nouveaux labels avec les sauts de ligne
        ax.set_xticks(range(len(new_labels)))  # Définir les positions des ticks
        ax.set_xticklabels(new_labels, ha='center')  # Centrer les labels

    ax.spines['bottom'].set_color(color_chart)
    ax.spines['left'].set_color(color_chart)
    ax.tick_params(axis='x', colors=color_chart)
    ax.tick_params(axis='y', colors=color_chart)

    # Remove top and right spines (borders)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Ensure everything fits using tight_layout()
    fig.tight_layout()  # or use constrained_layout=True in subplots
    # Save plot to a BytesIO object
    buf = io.BytesIO()
    fig.savefig(buf, format='png', transparent =True)
    buf.seek(0)
    plt.close(fig)
    # Return the plot as a StreamingResponse
    return StreamingResponse(buf, media_type="image/png")

@app.get("/plot_pie/{data}/{theme}/{type_tableau}")
async def get_plot_pie(data, theme, type_tableau):
    json_data = json.loads(data)
    # Create your plot
    labels = json_data['labels']
    values = json_data['values'] # Example data

    # Create pie chart
    fig, ax = plt.subplots()
    
    threshold = 15
    # Appliquer la fonction de split sur tous les labels
    new_labels = [split_label(label, threshold) for label in json_data['labels']]
    
    color_chart = "white" #if theme == "dark" else "black"

    def absolute_value(val):
        a = round(val / 100 * sum(values))
        return f'{a}'

    if(type_tableau =="true"):
        ax.pie(values, autopct=absolute_value, shadow=True, startangle=90, textprops={'color':color_chart}, labeldistance=1.2, pctdistance=0.6)
    else:
        ax.pie(values, autopct='%1.1f%%', shadow=True, startangle=90, textprops={'color':color_chart}, labeldistance=1.2, pctdistance=0.6)


    plt.legend(new_labels, loc="best")

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')

    # Ensure labels are not cut off
    fig.tight_layout()  # or constrained_layout=True in subplots()

    # Save to BytesIO object
    buf = io.BytesIO()
    fig.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    plt.close(fig)

    # Return the image as a response
    return StreamingResponse(buf, media_type='image/png')

    
@app.get("/plot_line/{data}")
async def get_plot_line(data):
    json_data = json.loads(data)
    # Create your plot
    labels = json_data['labels']
    values = json_data['values'] # Example data
    # explode = (0, 0.1)  # Explode one slice for emphasis

    # Create pie chart
    fig, ax = plt.subplots()
    ax.plot(labels, values, marker='o', linestyle='-', color='b', label='Données')
    
    ax.set_xticklabels(json_data['labels'], rotation=45, ha='right') 
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')

    # Ensure labels are not cut off
    fig.tight_layout()  # or constrained_layout=True in subplots()

    # Save to BytesIO object
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    # Return the image as a response
    return StreamingResponse(buf, media_type='image/png')

@app.get("/get_plot_osgood/{data}/{poles_gauche}/{poles_droite}/{theme}")
async def get_plot_osgood(data, poles_gauche, poles_droite, theme):
    data = json.loads(data)
    poles_gauche=poles_gauche.split(',')
    poles_droite=poles_droite.split(',')
    df = pd.DataFrame(data)
    if len(poles_gauche) != df.shape[1] or len(poles_droite) != df.shape[1]:
        raise ValueError("Le nombre de pôles doit correspondre au nombre de dimensions sémantiques.")

    color_axes = 'white' if theme == 'dark' else 'black'
    color_profil = 'orange' if theme == 'dark' else 'blue'
    color_value = 'black' if theme == 'dark' else 'black'
    
    # Moyenne pour chaque dimension sémantique
    semantiques_gauche_df = df.mean()

    new_labels_gauche = [split_label(label, 15) for label in poles_gauche]
    new_labels_droite = [split_label(label, 15) for label in poles_droite]

    # Création du graphique
    fig, ax1 = plt.subplots(figsize=(8, 4))

    # Tracé des points et lignes pour le premier axe y
    ax1.plot(semantiques_gauche_df.values, new_labels_gauche, marker='o', linestyle='-', color=color_profil)
    # Affichage de chaque valeur moyenne à côté des points
    for i, value in enumerate(semantiques_gauche_df.values):
        ax1.text(value - 3, i, f"{value:.1f}", color=color_value, va='bottom', ha='right', fontsize=8,  
                 bbox=dict(facecolor='lightgray', edgecolor='lightgray', boxstyle='round,pad=0.2', alpha=1.0))  # Ajout d'un fond gris clair

    ax1.set_xlim(0, 100)
    # ax1.grid(True, axis='x')
    plt.subplots_adjust(left=0.2, right=0.8)
    ax1.tick_params(axis='x', colors=color_axes)
    ax1.tick_params(axis='y', colors=color_axes, pad=10)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)

    # Ajout du second axe y
    ax2 = ax1.twinx()
    ax2.plot(semantiques_gauche_df.values, new_labels_droite, marker='o', linestyle='-', color=color_profil)
    ax2.grid(True, axis='y', color='lightgray', alpha=0.7, zorder=99)
    ax2.spines['bottom'].set_color(color_axes)
    ax2.tick_params(axis='y', colors=color_axes, pad=10)

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)

    # Sauvegarder l'image dans un buffer BytesIO
    buf = io.BytesIO()
    fig.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    plt.close(fig)

    # Retourner l'image comme réponse
    return StreamingResponse(buf, media_type='image/png')

@app.get("/get_plot_notation/{data}/{theme}/{max_stars}/{star_size}/{type_tableau}")
async def get_plot_notation(data, max_stars, theme, star_size, type_tableau, star_color='orange', space_between=5):
    
    data = list(map(int, data.split(',')))  # Convert votes to integers
    label = " vote(s)"
    if (type_tableau == "false"):
        total = sum(data)
        data = [round((x / total) * 100, 2) for x in data] # Convert each value to percentage with 2 decimal places
        label = "% vote(s)"
    # Set colors for different parts
    stars_color = 'orange' if theme == 'dark' else 'royalblue'  #star_color
    votes_color = 'white' if theme == 'dark' else 'black' 
    votes_rep_color = 'moccasin' if theme == 'dark' else 'lightsteelblue'

    num_levels = int(max_stars)  # Number of levels corresponds to the max stars
    levels = np.arange(1, num_levels + 1)  # Evaluation levels from 1 to max_stars
    
    fig, ax = plt.subplots(figsize=(9, 6))  # Adjusted figure size
    
    # Normalize votes for text width
    max_votes = max(data) if max(data) > 0 else 1  # Avoid division by zero

    # Display each level in descending order
    for i, (level, votes) in enumerate(zip(reversed(levels), reversed(data))):
        # Full stars for each level
        full_stars = level
        stars = '★' * full_stars + '☆' * (int(max_stars) - full_stars)  # Create filled and empty stars

        votes_rep = '  |' + '▪' * int((votes / max_votes) * 10)  # Scale to a 0-10 range for representation
        
        # Position the text combined
        y_position = num_levels - i - 0.5
        
        # Display stars with their color
        ax.text(0.5, y_position, stars, fontsize=star_size, color=stars_color, va='center')
        
        # Display votes text with its color
        ax.text(6, y_position, f"{votes}{label}", fontsize=12, color=votes_color, va='center', ha='center')
        
        # Display representation of votes with its color
        ax.text(7, y_position, votes_rep, fontsize=16, color=votes_rep_color, va='center')

    # Adjust limits to fit everything
    ax.set_xlim([0, 12])  # Wide enough limit for all items
    ax.set_ylim([0, num_levels])  # Adjust y limits to include all star levels
    
    # Hide unnecessary axes
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Sauvegarder l'image dans un buffer BytesIO
    buf = io.BytesIO()
    fig.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    # Retourner l'image comme réponse
    return StreamingResponse(buf, media_type='image/png')

@app.get("/get_plot_satisfaction/{data}/{satisfaction_levels}/{theme}/{type_tableau}")
async def get_plot_satisfaction(data, satisfaction_levels, theme, type_tableau):

    data = list(map(int, data.split(',')))  # Convert votes to integers
    satisfaction_levels = list(map(str, satisfaction_levels.split(',')))  # Convert levels to strings
    if (len(satisfaction_levels)==5):
        smileys = [mpimg.imread(f'images/smiley_{i+1}.png') for i in range(5)]
    elif (len(satisfaction_levels)==7):
        smileys = [mpimg.imread(f'images/smiley_{i}.png') for i in range(7)]

    fig, ax = plt.subplots(figsize=(8, 6))
    # bars = ax.bar(satisfaction_levels, data, color='lightsteelblue')

    if (type_tableau == "false"):
        percentage_data = [(value / sum(data)) * 100 for value in data] # Convert each value to a percentage
        percentage_data = [round(value, 2) for value in percentage_data] # Round each value to 2 decimal places
        bars = ax.bar(satisfaction_levels, percentage_data, color='lightsteelblue')
        # Add value labels on top of each bar
        for i, value in enumerate(percentage_data):
            plt.text(i, value -1, str(value)+'%', ha='center', va='top', color="black", fontsize=10)
        ax.set_ylim(0, max(percentage_data) * 1.2)  # Ajuste la marge en haut (1.4 pour 20% d'espace au-dessus des barres)
    else:
        bars = ax.bar(satisfaction_levels, data, color='lightsteelblue')
        for i, value in enumerate(data):
                plt.text(i, value - 2, str(value), ha='center', va='top', color="black", fontsize=10)
        # Ajuster les limites verticales de l'axe pour inclure les images
        ax.set_ylim(0, max(data) * 1.2)  # Ajuste la marge en haut (1.4 pour 40% d'espace au-dessus des barres)



    # Ajouter les smileys sur les barres
    for bar, smiley in zip(bars, smileys):
        # Créer une annotation avec l'image
        imagebox = OffsetImage(smiley, zoom=0.5)  # Ajustez `zoom` pour la taille de l'image
        ab = AnnotationBbox(imagebox, (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                            frameon=False, box_alignment=(0.5, 0))  # Centrer au-dessus de la barre
    
        # Ajouter l'image au graphique
        ax.add_artist(ab)

    nb_labels = len(satisfaction_levels)
    
    # Seuil pour scinder les labels sur deux lignes
    if nb_labels > 5:
        new_labels = [split_label(label, 20) for label in satisfaction_levels]
        ax.set_xticklabels(new_labels, ha='right', rotation=45)
    else:
        # Threshold adjustment based on the number of labels
        match nb_labels:
            case value if value < 3:
                threshold = 20
            case value if value < 5:
                threshold = 15
            case _:
                threshold = 10
        
        # Apply the splitting function to all labels
        new_labels = [split_label(label, threshold) for label in satisfaction_levels]
        ax.set_xticks(range(len(new_labels)))  # Set tick positions
        ax.set_xticklabels(new_labels, ha='center')  # Center the labels
    
    # Customize the chart appearance
    if theme == "dark":
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
    else:
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
    
    # Keep the axes visible
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Don't remove the x-ticks or the labels will disappear
    # ax.set_xticks([]) <- Remove this line

    plt.tight_layout()  # Adjust layout to fit labels

    
    # Sauvegarder l'image dans un buffer BytesIO
    buf = io.BytesIO()
    fig.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    # Retourner l'image comme réponse
    return StreamingResponse(buf, media_type='image/png')

@app.get("/get_plot_grille/{data}/{levels}/{items}/{theme}/{type_tableau}")
async def get_plot_grille(data, levels, items, theme, type_tableau):
    if(theme =="dark"):
        theme_color="white"
    else:
        theme_color="black"

    data = json.loads(data)
    levels = list(map(str, levels.split(',')))
    levels = [split_label(level, 12) for level in levels]
    items = list(map(str, items.split(',')))
    items = [split_label(item, 20) for item in items]

    data = np.array(data)
    # Convert each row to percentages
    if (type_tableau == "false"):
        percentage_data = (data / data.sum(axis=1, keepdims=True)) * 100 
        data = np.round(percentage_data, 2) # Rounded to 2 decimal places for readability
    
    fig, ax = plt.subplots(figsize=(10, 6))

    im, cbar = heatmap(data, items, levels, ax=ax, cmap="YlGn", cbarlabel="", theme_color=theme_color)
    texts = annotate_heatmap(im, valfmt="{x:.0f}") if type_tableau == "true" else annotate_heatmap(im, valfmt="{x:.2f}%")

    fig.tight_layout()
 
    buf = io.BytesIO()
    fig.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)

    return StreamingResponse(buf, media_type='image/png')


@app.get("/get_plot_wordcloud/{idQuestionnary}/{idQuestion}")
async def get_plot_wordcloud(idQuestionnary: int, idQuestion: int):
    reponses=[]
    query = "SELECT * from results where id_questionnary = $1"
    params = (idQuestionnary)
    records = await postgres_select_query(query, params)
    for record in records:
        content = json.loads(record[1])
        reponse =content[0]['questions'][idQuestion]['reponse']
        reponses.append(reponse)

    # Fusionner toutes les reponses en une seule
    aggregated_reponses = " ".join(reponses)
    # Download French stop words
    nltk.download('stopwords')
    french_stopwords = set(stopwords.words('french'))
    english_stopwords = set(stopwords.words('english'))

    # Générer le nuage de mots
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        stopwords=french_stopwords,
        collocations=False
    ).generate(aggregated_reponses)

    # Créer la figure Matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    # Ajuster la disposition
    fig.tight_layout()

    # Enregistrer l'image dans un buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    buf.seek(0)  # Revenir au début du buffer
    plt.close(fig)

    return StreamingResponse(buf, media_type='image/png')


@app.get("/get_report/{idQuestionnary}/{idQuestion}")
def get_images(idQuestionnary, idQuestion):
    images = []
    for i in range(3):  # Adjust the range as needed
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [i, i+1, i+2])  # Example plot
        buf = io.BytesIO()
        fig.savefig(buf, format="png", transparent=True, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        # Convert the image to Base64
        images.append(base64.b64encode(buf.read()).decode('utf-8'))
    return {"images": images}



@app.get("/get_type_question/{idQuestionnary}/{idQuestion}")
async def get_type_question(idQuestionnary:int, idQuestion:int):
    type_question=""
    query = "SELECT * from results where id_questionnary = $1"
    params = (idQuestionnary)
    records = await postgres_select_query(query, params)
    content = json.loads(records[0]['content_result'])
    type_question =content[0]['questions'][idQuestion]['type']
    return type_question

@app.get("/save_commentaire/{idQuestionnary}/{idQuestion}/{comment}")
async def get_type_question(idQuestionnary:int, idQuestion:int, comment):
    query = "INSERT INTO comment (id_questionnary, id_question, comment) VALUES ($1, $2, $3) RETURNING id_comment"
    params = (idQuestionnary, idQuestion, comment)
    last_id = await postgres_insert_query(query, *params)
    return (last_id)

@app.get("/update_commentaire/{idQuestionnary}/{idQuestion}/{comment}")
async def get_type_question(idQuestionnary:int, idQuestion:int, comment):
    query = "UPDATE comment SET comment = $3 WHERE id_questionnary = $1 and id_question = $2"
    params = (idQuestionnary, idQuestion, comment)
    last_id = await postgres_update_query(query, *params)
    return (last_id)

@app.get("/get_commentaire/{idQuestionnary}/{idQuestion}")
async def get_commentaire(idQuestionnary:int, idQuestion:int):
    query = "SELECT * from comment where id_questionnary = $1 and id_question = $2"
    params = (idQuestionnary, idQuestion)
    try:
        result = await postgres_select_query(query, *params)
        return result
    except Exception as e:
        return {"error": str(e)}