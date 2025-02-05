import asyncio
import asyncpg
import random
import json
from copy import deepcopy
from read_line_txt import *

db_params = {
        'database': 'quaeroquesto',
        'user': 'postgres',
        'password': 'nBl030130!',
        'host': 'localhost',
        'port': '5432',
    }

async def postgres_insert_query(query, data):
    try:
        conn = await asyncpg.connect(**db_params)
        last_id = await conn.fetchval(query, *data)
        await conn.close()
        return last_id
    except asyncpg.exceptions.ConnectionDoesNotExistError:
        print("Connection was closed unexpectedly. Retrying...")
        await asyncio.sleep(1)  # Wait before retrying
        return await postgres_insert_query(query, data)  # Retry the query
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

async def generer_jeu_data(n):
	compt=0
	for num in range(n):
		compt+=1
		questionnaire = json.loads(questionnaire_json)
		questionnaire_avec_reponses = generer_reponses_aleatoires(deepcopy(questionnaire), compt)
		result = json.dumps(questionnaire_avec_reponses)  # Keep as string
		# Use parameterized query to avoid SQL injection
		query = "INSERT INTO results (content_result, id_questionnary) VALUES ($1, $2)"
		data = (result, 1)
		last_id = await postgres_insert_query(query, data)

def generer_reponses_aleatoires(questionnaire, compt):
	# Fonction pour générer une réponse aléatoire pour chaque question
	for questionnaire_data in questionnaire:
		for question in questionnaire_data['questions']:
			if question['type'] == "EditFermeeSimpleComponent":
				# Une seule modalité a isChecked à True
				for modalite in question['modalites']:
					modalite['isChecked'] = False
				choix = random.choice(question['modalites'])
				choix['isChecked'] = True
				print(f"EditFermeeSimpleComponent choice: {choix}")
				print("---------------------------------------------------------------------------------------")
			elif question['type'] == "EditFermeeMultipleComponent":
				# Plusieurs modalités peuvent avoir isChecked à True
				for modalite in question['modalites']:
					modalite['isChecked'] = random.choice([True, False])
					print(f"EditFermeeMultipleComponent choice: {modalite}")
					print("---------------------------------------------------------------------------------------")
			elif question['type'] == "EditEchelleComponent":
				# Valeur comprise entre 0 et 100
				for semantique in question['semantiques']:
					semantique['valeur'] = str(random.randint(0, 100))
					print(f"EditEchelleComponent choice: {semantique}")
					print("---------------------------------------------------------------------------------------")
			elif question['type'] == "EditGrilleComponent":
				# Réponse comprise entre 1 et 5
				for ligne in question['lignes']:
					ligne['reponse'] = random.randint(1, 5)
					print(f"EditGrilleComponent choice: {ligne}")
					print("---------------------------------------------------------------------------------------")
			elif question['type'] == "EditSatisfactionComponent":
				# Note comprise entre 1 et 7
				question['note'] = str(random.randint(1, 5))
				print(f"EditSatisfactionComponent choice: {question}")
				print("---------------------------------------------------------------------------------------")
			elif question['type'] == "EditNotationComponent":
				# Note comprise entre 1 et 10
				question['note'] = random.randint(1, 10)
				print(f"EditNotationComponent choice: {question}")
				print("---------------------------------------------------------------------------------------")
			elif question['type'] == "EditOuverteComponent":
				question['reponse'] = lire_ligne("./generators/reponses_esprit_competition.txt", compt)
		print("==========================================================================================")
			

	return questionnaire


# Exemple de questionnaire
questionnaire_json = '''
[
	{
		"intitule": "Pratiques sportives",
		"date": "2024-12-11T19:00:19.088Z",
		"questions": [
			{
				"type": "EditFermeeSimpleComponent",
				"obligatoire": "obligatoire",
				"isCollapse": false,
				"question": "Pratiquez-vous un ou plusieurs sports ?",
				"modalites": [
					{
						"position": 1,
						"libelle": "Régulièrement",
						"isChecked": false
					},
					{
						"position": 2,
						"libelle": "De temps en temps sans régularité",
						"isChecked": false
					},
					{
						"position": 3,
						"libelle": "Occasionnellement",
						"isChecked": false
					},
					{
						"position": 4,
						"libelle": "Rarement",
						"isChecked": false
					},
					{
						"position": 5,
						"libelle": "Pas du tout",
						"isChecked": false
					}
				],
				"branchements": []
			},
			{
				"type": "EditFermeeMultipleComponent",
				"obligatoire": "obligatoire",
				"ordonnee": "Oui",
				"maxReponses": 7,
				"isCollapse": false,
				"question": "Lequel ou lesquels ?",
				"modalites": [
					{
						"position": 1,
						"libelle": "Football",
						"isChecked": false
					},
					{
						"position": 2,
						"libelle": "Basketball",
						"isChecked": false
					},
					{
						"position": 3,
						"libelle": "Volleyball",
						"isChecked": false
					},
					{
						"position": 4,
						"libelle": "Tennis",
						"isChecked": false
					},
					{
						"position": 5,
						"libelle": "Judo",
						"isChecked": false
					},
					{
						"position": 6,
						"libelle": "Karaté",
						"isChecked": false
					},
					{
						"position": 7,
						"libelle": "Autres",
						"isChecked": false
					}
				],
				"branchements": []
			},
			{
				"type": "EditNotationComponent",
				"obligatoire": true,
				"isCollapse": false,
				"nbStars": 10,
				"note": 0,
				"question": "Comment jugez-vous la politique de la ville de Paris en matière de sport, 1 étoile voulant dire qu elles ne sont pas du tout à la hauteur de vos attentes ?"
			},
			{
				"type": "EditEchelleComponent",
				"obligatoire": "obligatoire",
				"isCollapse": false,
				"question": "Comment jugez-vous les infrastructures publiques sportives auxquelles vous pouvez accéder à proximité de votre domicile ?",
				"semantiques": [
					{
						"position": 1,
						"libelleGauche": "Pas du tout faciles daccès",
						"libelleDroit": "Plutôt faciles daccès"
					},
					{
						"position": 2,
						"libelleGauche": "Plutôt chères voire très chères",
						"libelleDroit": "Pas chères voire gratuites"
					},
					{
						"position": 3,
						"libelleGauche": "Plutôt mal équipées",
						"libelleDroit": "Bien équipées"
					},
					{
						"position": 4,
						"libelleGauche": "Mal entretenues",
						"libelleDroit": "Bien entretenues"
					},
					{
						"position": 5,
						"libelleGauche": "Trop fréquentées",
						"libelleDroit": "Pas trop fréquentées"
					}
				],
				"branchements": []
			},
			{
				"type": "EditSatisfactionComponent",
				"obligatoire": "obligatoire",
				"isCollapse": false,
				"note": "",
				"echelle": "1",
				"echelle_list": [
					"Très Insatisfait",
					"Plutôt Insatisfait",
					"Moyennement Satisfait",
					"Plutôt Satisfait",
					"Très Satisfait"
				],
				"question": "Comment évaluez-vous votre satisfaction concernant votre pratique sportive ?"
			},
			{
				"type": "EditGrilleComponent",
				"obligatoire": "obligatoire",
				"isCollapse": false,
				"question": "Veuillez indiquer votre niveau daccord avec chacune des propositions suivantes ?",
				"lignes": [
					{
						"position": 1,
						"libelle": "Le sport allonge la durée de vie"
					},
					{
						"position": 2,
						"libelle": "Le sport est avant tout une source de plaisir"
					},
					{
						"position": 3,
						"libelle": "Le sport exige beaucoup de volonté"
					}
				],
				"colonnes": [
					{
						"position": 1,
						"libelle": "Pas du tout d'accord"
					},
					{
						"position": 2,
						"libelle": "Assez peu d'accord"
					},
					{
						"position": 3,
						"libelle": "Moyennement d'accord"
					},
					{
						"position": 4,
						"libelle": "Plutôt d'accord"
					},
					{
						"position": 5,
						"libelle": "Tout à fait d'accord"
					}
				],
				"branchements": []
			}
		]
	}
]
'''

if __name__ == "__main__":
    asyncio.run(generer_jeu_data(100))
	