import os
import openai
import json

def get_libelle_question():
  openai.api_base = "http://localhost:7000/v1" # point to the local server
  openai.api_key = "not-needed" # no need for an API key
  system_content = "En tant que chargé d'études, tu réalises un sondage auprès d'un échantillon de personnes sur leurs pratiques sportives."
  user_content = "Peux-tu poser une question sans les réponses possibles pour mesurer la fréquence de l'activité sportive durant les 3 prochains mois d'une personne."
  completion = openai.ChatCompletion.create(
    model="local-model", # this field is currently unused
    messages=[
      {"role": "system", "content": system_content},
      {"role": "user", "content": user_content}
    ],
    temperature=0.4
  )
  response = completion.choices[0].message
  return response

def get_modalites_question(question):
  openai.api_base = "http://localhost:7000/v1" # point to the local server
  openai.api_key = "not-needed" # no need for an API key
  system_content = "Voici une question posée dans le cadre d'un sondage auprès d'un échantillon de personnes sur leurs pratiques sportives :  "+question
  user_content = "Peux-tu générer sous forme de liste ordonnée les différentes possibilités de réponse."
  completion = openai.ChatCompletion.create(
    model="local-model", # this field is currently unused
    messages=[
      {"role": "system", "content": system_content},
      {"role": "user", "content": user_content}
    ],
    temperature=0.4
  )

  response = completion.choices[0].message
  # response = json.loads(get_modalites_json(str(liste_propositions)))
  return response

def get_modalites_json(liste_propositions):
  openai.api_base = "http://localhost:7000/v1" # point to the local server
  openai.api_key = "not-needed" # no need for an API key
  system_content = "'''"+str(liste_propositions)+"'''"
  user_content = "Peux-tu générer une variable de type JSON avec ces différentes propositions"
  completion = openai.ChatCompletion.create(
    model="local-model", # this field is currently unused
    messages=[
      {"role": "system", "content": system_content},
      {"role": "user", "content": user_content}
    ],
    temperature=0.4
  )

  response = completion.choices[0].message
  return response