# Projet 2 - Web Scraping des Livres

## Description
Ce projet permet de scraper les données de livres à partir du site **Books to Scrape**. Il extrait des informations des livres. Les données récupérées sont ensuite sauvegardées dans un fichier CSV pour une analyse ultérieure.

## Fonctionnalités
- Extraction des données
- Téléchargement des images miniatures des livres
- Enregistrement des données dans un fichier CSV

## Prérequis
Avant de pouvoir exécuter ce projet, assurez-vous d'avoir les outils suivants installés sur votre machine :
- [Python  3.13.0](https://www.python.org/)
- Les bibliothèques Python suivantes :
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  
Vous pouvez installer les dépendances nécessaires en utilisant le fichier `requirements.txt` :

pip install -r requirements.txt


# INSTALLATION : 

Clonez ce dépôt sur votre machine locale :

Copier le code
git clone https://github.com/quentintaile/projet-2---Final.git

Accédez au répertoire du projet :
cd projet-2---Final

Installez les dépendances :
pip install -r requirements.txt

# UTILISATION

Une fois que tout est configuré, vous pouvez exécuter le script Python pour commencer à extraire les données :

Activer l'environnement : 
env\Scripts\activate  

Lancer le scrapping : 
python book_scrape.py

# CONTRIBUER

Forkez ce dépôt.
Créez une branche pour votre fonctionnalité (git checkout -b feature/amélioration).

Commitez vos modifications (git commit -m 'Ajout d'une nouvelle fonctionnalité').

Poussez votre branche (git push origin feature/amélioration).

Créez une Pull Request.