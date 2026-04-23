# PulsEvents: 
Concevez et déployez un système RAG pour la recommandation d'évènements culturels


## 1. Context et details

Ce projet a pour objectif de développer un système de RAG (Retrieval-Augmented Generation) permettant de recommander des événements culturels dans le département de l’Essonne.

### Objectifs

- Permettre à un utilisateur de poser des questions en langage naturel
- Rechercher les événements pertinents via similarité vectorielle
- Générer des réponses enrichies à partir du contexte

### Technologies utilisées
- Poetry 
- LangChain (Orchestrateur
- Mistral AI (LLM + embeddings)
- FAISS (base vectorielle)
- Streamlit (interface chat)



## 2. Prérequis
Avant de pouvoir utiliser ce projet, assurez-vous d'avoir installé les éléments suivants :

- **poetry** 
  - [Installer Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
  
- **Git** :
  - [Installer Git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)
 
Après avoir installé Git, placez-vous dans le dossier où vous souhaitez cloner le dépôt distant, puis exécutez la commande suivante :

 ```bash
git clone  https://github.com/hyhishem/PulsEvents_p10.git
 ```
Ensuite, accédez au dossier cloné :

 ```bash
cd PulsEvents_p10
 ```
Renommer le fichier 

 ```bash
.env.exemple -> .env
 ```

Puis ajoutez la clé API Mistral :

 ```bash
MISTRAL_API_KEY = xxxxx
 ```

## 3.  L'environnement virtuel

Installation des dépendances :

 ```bash
poetry install

 ```


## 4. Le pré-processing 
Cette étape permet de :

- nettoyer les données
- structurer les champs
- préparer le texte pour l’embedding
 
 ```bash
poetry run python script/data_pre_processing.py
 ```


## 5. Vectorisation des données 

Cette étape permet de :

- découper les textes en chunks
- génèrer les embeddings
- créer la base vectorielle FAISS liée à des metadonné

 ```bash
poetry run python script/vectorisation_mistral.py
  ```

## 6. Test unitaire 
Ce script permet de valider la qualité des données vectorisées. 

On verifie :

- La présence de documents dans la base
- Que les événements sont bien situés dans l’Essonne
- La cohérences des dates

 ```bash
poetry run pytest  -W ignore -v script/test.py
  ```

## 7. Utilisation d'un chat interactif RAG

Lancez l'interface utilisateur :


 ```bash
poetry run streamlit run app.py
  ```

## 8. Evaluer le comportement du chatbot

Pour évaluer le comportement du chatbot face à des requêtes hors de son domaine de compétence (événements culturels en Essonne), les questions suivantes peuvent être utilisé :

- Propose-moi un événement culturel dans les Yvelines. 
- Peux-tu me recommander un restaurant? 





