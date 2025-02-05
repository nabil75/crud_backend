import datetime
import ollama

desiredModel = "deepseek-r1:8b"
questionToAsk = "what are the best practices when it comes to questionnaire writing"
now = datetime.datetime.now()
print(now.year, now.month, now.day, now.hour, now.minute, now.second)
response = ollama.chat(model=desiredModel, messages = [
    {
        "role": "user",
        "content": """
        En tant que groupe de chercheurs en sciences sociales intéressé par les inégalités numériques. nous souhaitons créer un questionnaire pour :
        1- comprendre Les facteurs contribuant à l'accès inégal aux outils numériques et comment cela affecte les comportements sociaux et économiques des différentes populations.
        2- mesurer l'impact de l'accès aux outils numériques sur la participation économique, l'éducation et le lien social dans différents segments de la population.
        afin de mettre en place les actions qui nous permettront de Proposer des recommandations pour améliorer l'accès aux outils numériques et réduire les inégalités, afin de favoriser une meilleure inclusion sociale et économique..
        Les thèmes et sous thèmes à aborder dans cette étude sont les suivants :
        [{"name":"Accès aux outils numériques","selected":true,"subThemes":[{"name":"Disponibilité des équipements (ordinateurs, tablettes, smartphones)","selected":true},{"name":"Connectivité Internet (bande passante, coût)","selected":true},{"name":"Compétences numériques de base","selected":true},{"name":"Accessibilité pour les personnes en situation de handicap","selected":true}]},{"name":"Facteurs socio-économiques","selected":true,"subThemes":[{"name":"Niveau de revenu et d'éducation","selected":true},{"name":"Localisation géographique (rural vs urbain)","selected":true},{"name":"Statut socio-professionnel","selected":true},{"name":"Origine ethnique et diversité culturelle","selected":true}]},{"name":"Impact sur la participation économique","selected":true,"subThemes":[{"name":"Accès à l'emploi et au marché du travail","selected":true},{"name":"Entrepreneuriat et création d'entreprises","selected":true},{"name":"Utilisation des plateformes en ligne pour l'achat et la vente","selected":true},{"name":"Inclusion financière (services bancaires en ligne)","selected":true}]},{"name":"Impact sur l'éducation","selected":true,"subThemes":[{"name":"Accès à l'éducation en ligne","selected":true},{"name":"Efficacité des ressources éducatives numériques","selected":true},{"name":"Impact sur les résultats scolaires","selected":true},{"name":"Formations numériques pour adultes","selected":true}]},{"name":"Impact sur le lien social","selected":true,"subThemes":[{"name":"Utilisation des réseaux sociaux","selected":true},{"name":"Participation à des communautés ou forums en ligne","selected":true},{"name":"Impact sur les relations interpersonnelles","selected":true},{"name":"Sentiment d'appartenance à la société","selected":true}]},{"name":"Recommandations pour réduire les inégalités","selected":true,"subThemes":[{"name":"Programmes de subventions pour l'achat d'équipements","selected":true},{"name":"Initiatives de formation en compétences numériques","selected":true},{"name":"Amélioration de l'infrastructure Internet","selected":true},{"name":"Sensibilisation et campagne de communication","selected":true}]}]
        En tant que chargé d'études expert en conception de questionnaires auprès d'acteurs B2B, tu dois concevoir un questionnaire complet pour répondre aux objectifs de l'étude.
        Pour chacun de ces objectifs, tu dois concevoir des questions pertinentes et adaptées à notre public cible.
        Les questions doivent être claires, concises et non ambiguës. Elles pourront être posées sous forme de questions fermées à réponse unique, questions fermées à réponse multiple de questions ouvertes ou de questions sous forme de tableau.
        Le questionnaire doit être structuré de manière logique et cohérente, avec des transitions fluides entre les différentes sections.
        Les questions fermées devront être accompagnées de propositions de réponses pour faciliter le traitement des données. Les propositions de réponse doivent être énoncée de façon complète et leur nombre doit être limité pour ne pas surcharger le questionnaire.
        Durée maximale : 30 minutes
        Format : La structure du questionnaire doit être conforme à la norme JSON. 
            Le questionnaire devra contenir un titre et des questions.
            Chaque question devra contenir un titre, un type, des propositions de réponses, et une indication sur le caractère obligatoire ou non de la question.
            Les propositions de réponses ne devront pas être numérotées même si elles sont ordonnées.
            Dans le cas où le répondant doit apporter une appréciation sur différentes propositions celles-ci peuvent être regroupées dans un tableau avec en ligne les propositions et en colonne les options possibles.
            Dans le cas où la question ne contient une seule proposition, celle-ci est contenue dans le titre de la question et la liste des propositions est vide.
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
                            "titre": "Ceci est le libellé d'une Question  de type échelle",
                            "type": "echelle"
                            "options": [
                              	"Très intéressé",
                                "Plutôt intéressé",
                                "Moyennement intéressé",
                                "Peu intéressé",
                                "Pas du tout intéressé",
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
                        }
                }
        """},
])

OllamaResponse = response['message']['content']

print(OllamaResponse)
now_end = datetime.datetime.now()
print(now_end.year, now_end.month, now_end.day, now_end.hour, now_end.minute, now_end.second)