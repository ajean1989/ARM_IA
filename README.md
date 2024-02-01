# API 

Ce programme exécute l'API "IA" de l'application ARM qui a pour vocation la gestion du dataset ainsi que la mise à disposition du modèle de détection appelé par les utilisateurs.

On peut déployer l'API en exécutant le programme `autorun_api.sh` sous linux ou `autorun_api.bat` sous windows (cmd). 
Cette commande lance un container contenant python et toutes les dépendences nécéssaires. 
Les informations sensibles sont passées via des variables d'environnement.

Accédez au container via l'extension Dev-container : "Attach to a running container". Le volume créé dans docker-compose persiste les données entre le container et l'hôte de développement (`./app`). 

Lancer les tests dans le container depuis `/api`.

# Modèle de données

Dans le dossier {`mongodb`} se trouve le modèle de la base de données Mongo DB. 

# Branches

+ master : automatiquement pousser en production suite CI/CD
+ qualif : automatiquement pousser en pré-production suite CI/CD
+ dev : branche de développement

# Data

## Sample

Il y a quelques exemples de données pour faire des tests.

### Dataset dans gitignore

On peut ajouter d'autre dataset dans gitignore pour l'entrainement des modèles.

# Modeles

## Checkpoint dans gitignore 

télécharger les modèles yolov8x et yolov8x 
https://github.com/ultralytics/ultralytics/tree/main
On peut télécharger les checkpoints pour COCO ou openimageV7, détection ou segmentation. 

Le modèle yolov8n_custom<date> est un modèle finetuné pour détecter les articles (boite, bocal, contenant en général)

### Modele 1 (Projet E1)

Meilleur modèle à ce jour : yolov8n_custom201223_train9.pt
yolov8 fine-tuné avec un dataset custom de openimagev7 et SKU110k
Modèle de détection d'objet utilisé pour la création automatique du dataset.

### Modele 2 

Modèle qui servira à associer une image à un code barre. 

# Backend

Script d'anotation automatique. Il reçoit une image ou un flux vidéo en entrée et enregistre automatiquement dans la base de donnée dataset les images annotées des codes barre.

### API

Mise en place de l'API sur un VPS.
Cette API sert à communiquer avec les bases de données MongoDB pour la gestion des datasets et MariaDB pour analyse de données.
L'API est dans un conteneur Docker. Placer les fichers backend/api/ sur un hôte et lancer "```docker compose up```"/"```docker-compose up --force-recreate --build```".
Penser à configurer uvicorn pour la production dans le DockerFile. 

Pour le dev, lancer le build + run du container et accéder au container via l'extension Dev-container : "Attach to a running container". Le volume créé dans docker-compose persiste les données entre le container et l'hôte de développement (```./app```). 

Lancer les tests depuis le container depuis ```/api```.

# Trackers

Configuration des trackers utilisés avec YoloV8 pour l'identification des objets dans une séquence vidéo. 
Le tracker est utilisé dans l'algorithme d'annotation automatique. 
Pour qu'il fonctionne correctement, le modèle doit avoir un bon niveau de confidence dans sa détection.