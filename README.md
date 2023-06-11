# github_scraper

Ce programme a pour objectif de scraper les dépôts Github les plus populaires contenant le terme "json" dans leur nom, en classant ces dépôts par nombre d'étoiles. Les données sont ensuite insérées dans une base de données MongoDB pour un affichage ultérieur via une interface web simple.

## Instructions

1. Avoir une instance MongoDB en cours d'exécution localement. Il est possible d'utiliser MongoDB Compass pour une interface utilisateur graphique, et consulter la base de données.
2. Installer les librairies utilisées.
```pip install flask pymongo requests```
3. Lancer le programme Python et accéder à [localhost](http://localhost:5000)
