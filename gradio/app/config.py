import os

# API KEY

# Exemple de clés API autorisées (à remplacer par vos propres clés)
key = os.getenv("ARM_VPS1_API_KEY")
API_KEYS = {key: "admin"}

if os.getenv("NODE_ENV") == "production":
    DNS = "jacquenet.com"
if os.getenv("NODE_ENV") == "development":
    DNS = "jacquenet.traefik.me"
if os.getenv("NODE_ENV") == "test":
    DNS = "traefik"

# Mongo DB

# adresse_mongo = os.getenv("SERVER_VPS1_IP")
# adresse_mongo = "mongodb"
# port_mongo = 27017
# user_mongo = os.getenv("USER_MONGODB")
# pass_mongo = os.getenv("PWD_MONGODB")

# Maria DB

# adresse_mongo = os.getenv("SERVER_VPS1_IP")
# adresse_maria = "mariadb"
# port_maria = 3306
# user_maria = os.getenv("USER_MARIADB")
# pass_maria = os.getenv("PWD_MARIADB")


