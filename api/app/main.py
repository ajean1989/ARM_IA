import json

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Annotated
from app.mongo import Mongo
from app.config import API_KEYS




# API KEY

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

# Fonction de validation de l'API key

async def validate_api_key(api_key = Depends(api_key_header)):
    if api_key in API_KEYS:
        return api_key
    # code 403 automatiquement retourné par APIKeyHeader 


app = FastAPI(
    title="API ARMarket - OpenAPI 3.0",
    description="API ARMarket for VPS - Link with dataset and datawarehouse - E1 Project.",
    servers=[{"name" : "5.195.7.246"}],
    openapi_tags=[{"name" : "dataset"},
                  {"name", "datawarehouse"}],
    dependencies=[Depends(validate_api_key)],
    root_path="/api-ia"
)

# Connexion Mongo DB
def mongo_connect():        # Permet d'overwrite pour les tests
    return Mongo(False)



# Routes

@app.get("/")
async def read_root():
    return {"Hello": "World"}




# Interact with Mongo DB

@app.get("/dataset/{id}")
async def get_dataset(id : str, mg : Annotated[Mongo, Depends(mongo_connect)]):

    zip_path = mg.get_dataset(int(id))

    if zip_path == False :
        mg.client.close()
        raise HTTPException(status_code=401, detail="ID inexistant ou vide")

    try:
        mg.client.close()
        return FileResponse(zip_path, media_type="application/zip")
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Fichier ZIP non trouvé")


@app.post("/dataset/frames/")
async def add_frame(mg : Annotated[Mongo, Depends(mongo_connect)], files: list[UploadFile] = File(...)):

    try:
        if len(files) != 3:
            return JSONResponse(content={"error": "array must have 3 binaries elements"}, status_code=405)
        if not files[0].filename.lower().endswith((".png", ".jpg", ".jpeg")):
            return JSONResponse(content={"error": "L'image doit avoir une extension .png, .jpg ou .jpeg"}, status_code=405)
        
        metadata = eval(files[2].file.read().decode("utf-8"))
        # metadata = json.loads(files[2].file.read().decode("utf-8"))

        img = files[0].file.read()
        anotation = files[1].file.read()
        
        mg.set_img(img, anotation, dataset_id = metadata["dataset"], dataset_extraction = metadata["dataset_extraction"], pretreatment = metadata["pretreatment"], data_augmentation = metadata["data_augmentation"])

        return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)
    
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")




class Update(BaseModel):
    id : str
    query: dict
    test : bool

@app.put("/dataset/frames/")
async def update_frame(mg : Annotated[Mongo, Depends(mongo_connect)], update : Update):

    try : 
        update = update.model_dump()

        for i in update["query"].keys() :
            if i not in ["name", "pre_treatment", "data_augmentation", "dataset", "training_data"] :
                return JSONResponse(content={"error": f"Le champ {i} ne peut pas être modifié."}, status_code=405)

        # possible de rajouter dataset id / data augmentation / test à set_img
        mg.update_frame(update["id"], update["query"])


        return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)
    
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")
    

@app.delete("/dataset/frames/{id}")
async def delete_frame(mg : Annotated[Mongo, Depends(mongo_connect)], id: str):

    if len(id) != 24 :
        mg.client.close()
        raise HTTPException(status_code=405, detail="ID must have 24-character hex string")

    response = mg.delete_frame(id)

    if response :
        mg.client.close()
        return JSONResponse(content={"message": "Élément supprimé avec succès"}, status_code=200)
    else :
        mg.client.close()
        raise HTTPException(status_code=405, detail="ID inexistant")
    
 

