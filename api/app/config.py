import os

# API KEY

# Exemple de clés API autorisées (à remplacer par vos propres clés)
key = os.getenv("ARM_VPS1_API_KEY")
API_KEYS = {key: "admin"}

# Mongo DB

# adresse_mongo = os.getenv("SERVER_VPS1_IP")

#local
# adresse_mongo = "localhost"
#prod
adresse_mongo = "mongodb"
port_mongo = 27017
user_mongo = os.getenv("USER_MONGODB")
pass_mongo = os.getenv("PWD_MONGODB")


