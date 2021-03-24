# American_dream
Projet visualisation

## Composition du répertoire

- Data: fichier permettant de stocker la data au format csv
  *01_raw: fichiers bruts initiaux

- SRC: Script permettant de traiter la donner
  *d00_utils: script contenant les fonctions permettant la connexion avec sqlite et petites fonctions récurrentes utilisées dans les notebooks, par exemple md() permet d'écrire du markdown dans les cellules de code
  *d01_data : script sql de création des tables et base de donnée sqlite, ces fichiers sont générés lors de l'execution du premier notebook
  
- Notebook: notebook présentant le travail
* Career_visualization: notebook de présentation des représentations répondant aux question
* Career_cleaning: notebook de présentation du nettoyage de données

## HOW TO

* lancer Career_visualization, l'export en sqlite se fait automatiquement à la fin
* lancer Career_cleaning, l'import en sqlite se fait automatiquement au début pour créer les dataframes