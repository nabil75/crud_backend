from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os
import agentops
from archive.Agent_Tools import SearchWebTool
import json

agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))

# Initialize the tool
search_tool = SearchWebTool()


# Chargement des variables d'environnement
load_dotenv()

llm_strategy_expert = LLM("gpt-4o", temperature=0.2, api_key=os.getenv("OPENAI_API_KEY"), top_p=0.2, max_tokens=10000)
llm_question_formulator = LLM("gpt-4o", temperature=0.2, api_key=os.getenv("OPENAI_API_KEY"), top_p=0.2, max_tokens=10000)
llm_final_reviewer = LLM("gpt-4o", temperature=0.2, api_key=os.getenv("OPENAI_API_KEY"), top_p=0.2, max_tokens=10000)


# Création des agents
# Définition du chercheur web
researcher = Agent(
    role='Chercheur Web et Analyste de Contexte',
    goal='Enrichir le contexte du projet avec des informations pertinentes du web et les synthétiser pour la création du questionnaire.',
    backstory="""Je suis un chercheur web spécialisé dans l'analyse approfondie de contextes 
    business. Ma mission est double : d'abord comprendre en profondeur le contexte initial 
    du projet, puis l'enrichir avec des informations pertinentes trouvées en ligne 
    (tendances du secteur, études similaires, meilleures pratiques). Je synthétise 
    ces informations de manière structurée pour faciliter la création d'un questionnaire 
    pertinent et complet.""",
    tools=[search_tool],
    verbose=True
)

# Define the manager agent
manager = Agent(
    role="Manager de projet",
    goal="Gérer le projet de création de questionnaire de manière efficace et de haute qualité.",
    backstory="""Vous êtes un gestionnaire de projet expérimenté, capable de diriger des projets complexes et de guider les équipes vers le succès. Votre rôle est de coordonner les efforts des membres de l'équipe, en veillant à ce que chaque tâche soit terminée à temps et à un niveau de qualité élevé.""",
    allow_delegation=True
)

# Définition de l'expert en stratégie
strategy_expert = Agent(
    llm=llm_strategy_expert,
    role='Expert en Stratégie de Questionnaire',
    goal='Concevoir une structure de questionnaire optimale en s\'appuyant sur le contexte',
    backstory="""Expert en méthodologie d'enquête avec une expertise particulière dans 
    la transformation de problématiques business en questionnaires structurés et 
    efficaces. Mon approche combine :
    - L'analyse du contexte initial du projet
    - La traduction de ces éléments en sections de questionnaire cohérentes et ciblées
    Je m'assure que chaque section du questionnaire serve un objectif précis et 
    contribue à la compréhension globale du sujet étudié.""",
    verbose=True
)

# Define the question formulator agent
question_formulator = Agent(
    llm= llm_question_formulator,
    role='Rédacteur de Questions',
    goal='Rédiger les questions spécifiques pour chaque section du questionnaire',
    backstory="""Expert en formulation de questions qui transforme les objectifs en questions 
        concrètes et efficaces. Maîtrise les différents types de questions (fermées, 
        ouvertes, échelles) et sait quand les utiliser."""
)


# Define the final reviewer agent
final_reviewer = Agent(
    llm= llm_final_reviewer,
    role='Assembleur du Questionnaire',
    goal='Assembler et finaliser le questionnaire complet',
    backstory="""Expert en mise en forme finale qui assure la cohérence globale du 
        questionnaire, vérifie l'enchaînement logique des questions et ajoute les 
        éléments nécessaires (introduction, transitions, conclusion)."""
)


# Tâche de recherche et d'enrichissement du contexte
task_search = Task(
    description="""Analyser le contexte du projet et l'enrichir avec des recherches web pertinentes :
    1. Analyser en profondeur le contexte initial du projet
    2. Identifier les domaines clés nécessitant un enrichissement
    3. Effectuer des recherches web ciblées pour :
       - Identifier les meilleures pratiques du secteur
       - Trouver des études similaires et leurs méthodologies
       - Repérer les tendances actuelles pertinentes
    4. Synthétiser toutes les informations de manière structurée pour le strategy_expert""",
    expected_output="""Un rapport détaillé comprenant :
    - Synthèse du contexte initial
    - Nouvelles informations pertinentes issues des recherches web
    - Analyse des implications pour la conception du questionnaire
    - Recommandations spécifiques pour les thématiques à explorer dans le questionnaire
    Le tout organisé de manière à faciliter le travail du strategy_expert""",
    agent=researcher
)


# Mise à jour de la tâche de structuration du questionnaire
task_structure = Task(
    description="""En utilisant le contexte fourni, définir la structure complète du questionnaire :
    1. Analyser le rapport fourni par le researcher
    2. Identifier les sections principales nécessaires pour répondre aux objectifs du projet
    3. Définir les objectifs précis de chaque section
    4. Préciser le type d'information à collecter dans chaque section
    5. Assurer l'alignement entre les sections et les objectifs globaux du projet""",
    expected_output="""Un plan détaillé du questionnaire comprenant :
    - Les sections identifiées, justifiées par le contexte et les recherches
    - Les objectifs spécifiques de chaque section
    - Le type d'information à collecter pour chaque section
    - Le format recommandé pour chaque type d'information
    - La justification de la structure proposée en lien avec les insights fournis""",
    agent=strategy_expert
)

task_questions = Task(
    description="""Pour chaque section identifiée, créer les questions spécifiques :
    1. Rédiger les questions en respectant les bonnes pratiques de conception de questionnaire (questions courtes, formulation neutre)
    2. Définir les modalités de réponse pour chaque question
    3. Veiller à l'ordre des questions dans chaque section (du général au spécifique, du simple au complexe)""",
    expected_output="""Pour chaque section :
    - Les questions rédigées
    - Les modalités de réponse associées
    - L'ordre des questions
    - Les instructions spécifiques si nécessaire""",
    agent=question_formulator
)

task_assembly = Task(
    description="""Assembler le questionnaire final :
    1. Organiser toutes les questions dans un format cohérent
    2. Ajouter les textes d'introduction et de transition
    3. Vérifier la fluidité et la logique de l'ensemble""",
    expected_output="""Le questionnaire complet en format json comprenant :
    - Le texte d'introduction
    - Les sections avec leurs questions
    - Les transitions entre les sections
    - La conclusion et les remerciements""",
    agent=final_reviewer
)

# Création du Crew
questionnaire_crew = Crew(
    agents=[strategy_expert, question_formulator, final_reviewer],
    tasks=[task_structure, task_questions, task_assembly],
    process=Process.sequential,
    verbose=True,
    api_key=os.getenv("OPENAI_API_KEY")
)

def create_questionnaire(project_context):
    """
    Crée un questionnaire complet à partir du contexte du projet
    
    Args:
        project_context (str): Description du contexte et des besoins du projet
    
    Returns:
        str: Le questionnaire final complet
    """
    result = questionnaire_crew.kickoff(
        inputs={
            "contexte_projet": project_context
        }
    )
    # the resuly should be returned as markdown text
    return result

if __name__ == "__main__":
    project_context = """
    Nous sommes une entreprise de fabrication de produits phytosanitaires et nous souhaitons créer un questionnaire pour comprendre les freins à l'achat de notre dernier produit Galatane 2000.
    Objectifs principaux :
    1. Mesurer le niveau de notoriété de notre produit Galatane 2000 auprès des agriculteurs
    1. Comprendre les habitudes d'achat et d'usage des produits phytosanitaires par les agriculteurs (critères de choix, fréquence d'achat, canaux de distribution privilégiés)
    2. Identifier les axes d'amélioration de notre produit Galatane 2000 pour mieux répondre aux besoins des agriculteurs (efficacité, prix, conditionnement, etc.)
    3. Identifier les concurrents principaux et les raisons de leur succès auprès des agriculteurs qui pourraient expliquer les freins à l'achat de Galatane 2000
    
    Public cible : Exploitants agricoles, distributeurs de produits phytosanitaires
    Durée maximale : 15 minutes
    Format : JSON
    """
    
    questionnaire = create_questionnaire(project_context)

    print(questionnaire)

    # enregistrer le questionnaire dans un fichier json
    with open("questionnaire.txt", "w") as file:
        file.write(str(questionnaire))