"""
Prérequis:
- cloner le répertoire
- créer un envrionnement virtuel 
- pip3 install les requierements
- INSTALLER Sqlite3 sur votre ordinateur
- pour lancer l'appli à la racine lancer run.py


Vous devez compléter l'API_modele_dem avec:
- un nouveau modèle représantant la table video (titre, longueur, channel) et ajouter des lignes à la base de données
- une méthode (requete d'API) pour obtenir toutes les vidéos d'une chaine
- une méthode pour obtenir tous les attributs d'une vidéo
- une méthode pour créer une vidéo
- une méthode pour supprimer une vidéo
- une méthode pour modifier le titre d'une vidéo


- une notion d'utilisateur (nom, email) qui possède une liste de chaines favorites
- une méthode pour obtenir toutes les vidéos favorites d'un utilisateur

Bonus:
un système de login et de token pour protéger la route delete video 

Conseil:
Les documentations aident: 
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/


"""