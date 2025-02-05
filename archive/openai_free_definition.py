from openai import OpenAI
import json

client = OpenAI(
  api_key="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"
)

stream = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": """
    En tant qu'un incubateur de startups et nous souhaitons créer un questionnaire pour comprendre les besoins des entrepreneurs en matière de financement
    Quels sont les thèmes et sous-thèmes à aborder dans ce questionnaire ?
    le résultat doit être un JSON avec les thèmes généraux et les sous-thèmes associés.
    Voici un exemple de structure du questionnaire au format JSON :
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

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
        

# # Collecte des morceaux de réponse
# response_text = ""

# for chunk in stream:
#     content = chunk.choices[0].delta.content
#     if content:  # Vérifier si le contenu n'est pas None
#         response_text += content

# # Extraction et affichage du JSON
# try:
#     start_index = response_text.index("{")
#     end_index = response_text.rindex("}") + 1
#     json_content = response_text[start_index:end_index]

#     # Charger le contenu JSON et afficher
#     questionnaire_json = json.loads(json_content)
#     print(json.dumps(questionnaire_json, indent=2, ensure_ascii=False))

# except (ValueError, json.JSONDecodeError):
#     print("Erreur : Impossible d'extraire le JSON.")