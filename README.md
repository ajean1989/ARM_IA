# Projet

Projet de fin d'étude de la certification Simplon : Développeur en Intelligence Artificielle. 
Ce projet est répartie en 5 thèmes: 
- Collecte des données : via SQL et NoSQL.
- Veille technologique sur un modèle d'IA : modèle de détection d'objet.
- Entrainement d' un modèle de détection d'objet, monitoring du modèle, déploiement continue et exposition via une API. 
- Interface web, pipeline CI/CD.
- Monitoring de l'application.

Ce projet est architecturé en micro-services. 3 repositories sont comoposés de plusieurs containers docker indépendants les uns des autres.  

# API 

Ce programme exécute l'API "IA" de l'application ARM qui a pour vocation la gestion du dataset ainsi que la mise à disposition du modèle de détection appelé par les utilisateurs.

On peut déployer l'API depuis les script du menu `./run/`. 

Accédez au container via l'extension Dev-container : "Attach to a running container". Le volume créé dans docker-compose persiste les données entre le container et l'hôte de développement (`./app`). 


# Modèle de données

Dans le dossier `mongodb` se trouve le modèle de la base de données Mongo DB. 

# Branches

+ master : automatiquement poussé en production suite CI/CD.
+ dev : branche de développement.

