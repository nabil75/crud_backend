from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="o1-preview",
    messages=[
    {"role": "user", "content": """
    Nous sommes un incubateur de startups et nous souhaitons créer un questionnaire pour comprendre les besoins des entrepreneurs en matière de financement
    Nous voulons nous appuyer sur cette étude pour mettre en place un cadre de mise en relation efficace entre startupers et financeurs (banques, état, investisseurs privés) .
    Objectifs privilégiés de l'étude :
    1.	Evaluer les besoins en financement des startups en fonction du métier, de la concurrence, du profil des fondateurs et de la maturité du projet.
    2.	Evaluer le niveau de connaissance des startups sur les dispositifs d'aide à l'innovation et à la création d'entreprise.
    3.	Identifier les freins à l'accès au financement pour les startups et les solutions envisagées pour les lever.
    4.	Comprendre les attentes des financeurs en matière de projet, de rentabilité, de risque et de durée de l'investissement.
    5.  Identifier les critères de sélection des financeurs et les éléments clés d'un dossier de financement réussi.
    
    En tant que chargé d'études expert en conception de questionnaires auprès d'acteurs B2B, tu dois concevoir un questionnaire complet pour répondre aux objectifs de l'étude.
    Pour chacun de ces objectifs, tu dois concevoir des questions pertinentes et adaptées à notre public cible.
    Les questions doivent être claires, concises et non ambiguës. Elles pourront être posées sous forme de questions fermées, de questions ouvertes ou de questions échelles.
    Le questionnaire doit être structuré de manière logique et cohérente, avec des transitions fluides entre les différentes sections.
    Les questions fermées devront être accompagnées de propositions de réponses pour faciliter le traitement des données. Les propositions de réponse doivent être énoncée de façon complète et leur nombre doit être limité pour ne pas surcharger le questionnaire.
    Public cible : Startups en phase d'amorçage, financeurs potentiels
    Durée maximale : 20 minutes
    Format : La structure du questionnaire doit être conforme à la norme JSON. Chaque question devra respecter les règles de syntaxe et de formatage suivantes, voici un exemple de structure de question en format JSON :
        {"titre" : "Ceci est le libéllé de la Question 1",
        "type" : ["fermee unique", "fermee multiple", "ouverte", "echelle", "Autre"],
        "propositions" : ["Très intéressé", "Plutôt intéressé", "Moyennement intéressé", "Peu intéressé", "Pas du tout intéressé"],
        "obligatoire" : ["oui", "non"]}
     """}
    ],


    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")