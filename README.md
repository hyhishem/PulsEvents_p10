# PulsEvents: 
Concevez et déployez un système RAG pour la recommandation d'évènements culturels


## 1. Context et details


## 2. Prérequis
Avant de pouvoir utiliser ce projet, assurez-vous d'avoir installé les éléments suivants :

- **poetry** 
  - [Installer Poetry]([https://docs.docker.com/compose/install/)](https://python-poetry.org/docs/#installing-with-the-official-installer)
  
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
Dans le fichier .env, mettre à jour  la clé api de Mistral :

 ```bash
MISTRAL_API_KEY = xxxxx
 ```

## 3.  L'environnement virtuel


 ```bash
poetry install

 ```


## 4. Le pré-processing 
 
 ```bash
poetry run python script/data_pre_processing.py
 ```


## 5. Vectorisation des données 


  ```bash
poetry run python script/vectorisation_mistral.py
  ```

## 6. Test unitaire 


  ```bash
poetry run python script/test.py
  ```

## 7. Utilisation d'un chat interactif RAG


  ```bash
poetry run streamlit run app.py
  ```

