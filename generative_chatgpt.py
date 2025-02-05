from openai import OpenAI
import json
import openai

async def auto_generate_questionnaire(role, objet_comprendre, objet_mesurer, finalite, selectedThemes, modelSelected):

    content = ""
    client = OpenAI()
    #     api_key="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"
    # )
    stream = client.chat.completions.create(
    model=modelSelected,
    store=True,
    messages=[
        {"role": "user", "content": """
        En tant que """+role+""" nous souhaitons créer un questionnaire pour :
        1- comprendre """+objet_comprendre+""" 
        2- mesurer """+objet_mesurer+""" 
        afin de mettre en place les actions qui nous permettront de """+ finalite+""".
        Les thèmes et sous thèmes à aborder dans cette étude sont les suivants :"""+
        selectedThemes
        +"""En tant que chargé d'études expert en conception de questionnaires auprès d'acteurs B2B, tu dois concevoir un questionnaire complet pour répondre aux objectifs de l'étude.
        Pour chacun de ces objectifs, tu dois concevoir des questions pertinentes et adaptées à notre public cible.
        Les questions doivent être claires, concises et non ambiguës. Elles doivent être formulées de manière à ne pas influencer les réponses des participants.
        Le questionnaire doit être structuré de manière logique et cohérente, avec des transitions fluides entre les différentes sections.
        Les questions fermées devront être accompagnées de propositions de réponses pour faciliter le traitement des données. Les propositions de réponse doivent être énoncée de façon complète et leur nombre doit être limité pour ne pas surcharger le questionnaire.
        Le nombre minimum de questions : 10
        Le questionnaire devra contenir un titre et des questions.
        Chaque question devra contenir un titre, un type, des propositions de réponses, et une indication sur le caractère obligatoire ou non de la question.
        Les propositions de réponses ne devront pas être numérotées même si elles sont ordonnées.
        Dans le cas où la question ne contient qu'une seule proposition, celle-ci est contenue dans le titre de la question et la liste des propositions est vide.
        Les types de questions possibles sont les suivants : fermée unique, fermée multiple, échelle, ouverte, tableau.
        Les questions fermées uniques et fermées multiples seront privilégiées quend les principales réponses sont connues. Les questions ouvertes seront utilisées pour des réponses plus libres et lorsque les possibilités de réponses sont nombreuses ou inconnues.
        Les questions de type échelle seront utilisées pour mesurer des opinions, des attitudes (prédispositions) ou des perceptions de marque, de produit ou tout autre concept abstrait.
        L'échelle utilisée devra reposer sur des sémantiques différentiels d'Osgood c'est à dire un ensemble d'opposition de adjectifs ou qualificatifs (ex : très agréable/très désagréable, facile à utiliser/difficile à utiliser, très bon pour la santé/très mauvais pour la santé ect.).
        Les questions de type Tableau seront utilisées dans le cas où le répondant doit apporter une appréciation sur différentes propositions qui seront alors regroupées dans un tableau avec en ligne les propositions et en colonne les options possibles.
        Format : La structure du questionnaire doit être conforme à la norme JSON. 
        Voici un exemple de structure au format JSON pour chaque type de questions :
            {
                "intitule_questionnaire": "Ceci est le libellé du Questionnaire",
                "questions": [
                    {
                        "titre": "Ceci est le libellé d'une Question  de type fermee multiple",
                        "type": "fermee multiple"
                        "options": [
                            "option de réponse 1",
                            "option de réponse 2",
                            "option de réponse 3",
                            "option de réponse 4",
                            "option de réponse 5",
                            "option de réponse 6",
                            "option de réponse 7",
                        ],
                        "obligatoire": [
                            "oui", 
                            "non"
                        ]
                    },
                    {
                        "titre": "Ceci est le libellé d'une Question  de type fermée unique",
                        "type": "fermee unique"
                        "options": [
                            "option de réponse 1",
                            "option de réponse 2",
                            "option de réponse 3",
                            "option de réponse 4",
                            "option de réponse 5",
                        ],
                        "obligatoire": [
                            "oui", 
                            "non"
                        ]
                    },
                    {
                        "titre": "Ceci est le libellé d'une Question  de type ouverte",
                        "type": "ouverte"
                        "obligatoire": [
                            "oui", 
                            "non"
                        ]
                    },
                    {
                        "titre": "Ceci est le libellé d'une Question  de type tableau",
                        "type": "tableau"
                        "propositions": [
                            "proposition1",
                            "proposition2",
                            "proposition3",
                            "proposition4",
                        ],
                        "options": [
                            "Pas du tout d'accord",
                            "Plutôt pas d'accord",
                            "Ni d'accord, ni pas d'accord",
                            "Plutôt d'accord",
                            "Tout à fait d'accord",
                        ],
                        "obligatoire": [
                            "oui", 
                            "non"
                        ]
                    },
                    {
                        "titre": "Ceci est le libellé d'une Question  de type echelle",
                        "type": "echelle",
                        "obligatoire": "oui",
                        "semantiques": [
                            {
                                "position": 1,
                                "libelleGauche": "sémantique gauche (ex : très agréable)",
                                "libelleDroit": "sémantique droit (ex : très désagréable)"
                            },
                            {
                                "position": 2,
                                "libelleGauche": "sémantique gauche (ex : très facile d'utilisation)",
                                "libelleDroit": "sémantique droit (ex : très difficile d'utilisation)"
                            },
                            {
                                "position": 3,
                                "libelleGauche": "sémantique gauche (ex : très bon pour la santé)",
                                "libelleDroit": "sémantique droit (ex : très mauvais pour la santé)"
                            }
                        ]
                        },
                    }
        """},
    ],
        stream=True,
    )

    # Collecte des morceaux de réponse
    response_text = ""

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:  # Vérifier si le contenu n'est pas None
            response_text += content

    # Extraction et affichage du JSON
    try:
        start_index = response_text.index("{")
        end_index = response_text.rindex("}") + 1
        json_content = response_text[start_index:end_index]

        # Charger le contenu JSON et afficher
        questionnaire_json = json.loads(json_content)
        # print(json.dumps(questionnaire_json, indent=2, ensure_ascii=False))
        content = json.dumps(questionnaire_json, indent=2, ensure_ascii=False)
        return content

    except (ValueError, json.JSONDecodeError):
        content="Erreur : Impossible d'extraire le JSON."
    except openai.RateLimitError as e:
        content = "Rate limit reached. Waiting..."
    
    return content

async def auto_generate_themes(role, objet_comprendre, objet_mesurer, finalite, modelSelected):
    content = ""
    client = OpenAI()
    #     api_key="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"
    # )

    stream = client.chat.completions.create(
    model=modelSelected,
    store=True,
    messages=[
   {"role": "user", "content": """
    En tant que """+role+""" nous souhaitons créer un questionnaire pour :
    1- comprendre """+objet_comprendre+""" 
    2- mesurer """+objet_mesurer+""" 
    afin de mettre en place les actions qui nous permettront de """+ finalite+""".
    Quels sont les thèmes et sous-thèmes à aborder dans ce questionnaire ?
    le résultat doit être un JSON avec les thèmes généraux et les sous-thèmes associés.
    Le résultat devra être au format JSON, voici la structure attendue :
      [
        {
          name: 'Thème 1',
          selected: false,
          subThemes: [
            { name: 'Sous-thème 1.1', selected: false },
            { name: 'Sous-thème 1.2', selected: false }
          ]
        },
        {
          name: 'Thème 2',
          selected: false,
          subThemes: [
            { name: 'Sous-thème 2.1', selected: false },
            { name: 'Sous-thème 2.2', selected: false }
          ]
        }
      ]
     """},
    ],
        stream=True,
        
    )
    
    # Collecte des morceaux de réponse
    response_text = ""

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:  # Vérifier si le contenu n'est pas None
            response_text += content

    return response_text


async def auto_generate_contexte(theme_contexte, modelSelected):
    content = ""
    client = OpenAI()
    #     api_key="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"
    # )
    message=""
    stream = client.chat.completions.create(
    model=modelSelected,
    store=True,
    messages=[
   {"role": "user", "content": """
    Je souhaite réaliser une étude sur  """+theme_contexte+""" et je voudrai que tu m'aides à cerner le sujet de mon étude. 
    Pour cela peux-tu compléter les phrases suivantes. Entre parenthèses sont indiqués les éléments de réponses attendus :
    1- En tant que ... (Qui veut réaliser cette étude ?). Il s'agit ici de définir le statut de la personne ou du groupe qui réalise l'étude.
    2- Nous souhaitons créer un questionnaire pour :
        21- Comprendre ... (Que voulez-vous comprendre grâce à cette étude?). Il s'agit ici d'identifier et de comprendre les éléments clés 
        à même d'expliquer les faits en rapport avec le sujet de l'étude.
        22- Mesurer ... (Que voulez-vous mesurer grâce à cette étude ?). Il s'agit ici de mesurer des dimensions propres au sujet étudié et 
        d'éclairer encore plus la compréhension et les actions à mener.
    3- Afin de mettre en place les actions qui nous permettront de … (A quoi servira cette étude ?). Il s'agit ici de définir les finalités de l'étude.
    Le résultat devra être au format JSON, voici la structure attendue :
      [
        {
            role: 'Qui veut réaliser cette étude ?',
            objet_comprendre: 'Que voulez-vous comprendre grâce à cette étude ?',
            objet_mesurer: 'Que voulez-vous mesurer grâce à cette étude ?',
            finalite: 'A quoi servira cette étude ?'
        }
      ]
     """},
    ],
        stream=True,
    )
    # Collecte des morceaux de réponse
    response_text = ""

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:  # Vérifier si le contenu n'est pas None
            response_text += content

    return response_text