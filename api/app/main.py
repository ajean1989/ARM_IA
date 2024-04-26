import json

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated

from app.mongo import Mongo
from app.config import API_KEYS
from app.log import log
from app.model import Model


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

# CORS

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes

@app.get("/")
async def read_root():
    try :        
        return {"Hello": "World"}
    except Exception as e : 
        raise HTTPException(status_code=422, detail=e)




# Interact with Mongo DB

@app.get("/dataset/{id}")
async def get_dataset(id : str, mg : Annotated[Mongo, Depends(mongo_connect)]):
    try:
        zip_path = mg.get_dataset(int(id))

        if zip_path == False :
            mg.client.close()
            raise HTTPException(status_code=406, detail="ID inexistant ou vide")

        mg.client.close()
        log.info('/dataset/{id} : Téléchargement zip.')
        return FileResponse(zip_path, media_type="application/zip")
        
    except Exception as e :
        log.debug(e)
        raise HTTPException(status_code=422, detail=f"{e}")
    # finally :
    #     mg.remove_temp_get_dataset()


@app.post("/dataset/frames/")
async def add_frame(mg : Annotated[Mongo, Depends(mongo_connect)], files: list[UploadFile] = File(...)):

    try:
        if len(files) != 3:
            log.debug(f"Il manque des éléments (3) => len : {len(files)} \n files : \n {files}")
            return JSONResponse(content={"error": "array must have 3 binaries elements"}, status_code=422)
        if not files[0].filename.lower().endswith((".png", ".jpg", ".jpeg")):
            log.debug(f"Invalide extension \n files : \n {files}")
            return JSONResponse(content={"error": f"L'image {files[0].filename.lower()} doit avoir une extension .png, .jpg ou .jpeg"}, status_code=422)
        
        # metadata = files[2].file.read().decode("utf-8")
        # metadata = eval(files[2].file.read().decode("utf-8"))
        # print(metadata)
        metadata = json.loads(files[2].file.read().decode("utf-8"))

        img = files[0].file.read()
        anotation = files[1].file.read()
        
        mg.set_img(img, anotation, dataset_id = metadata["dataset"], dataset_extraction = metadata["dataset_extraction"], pretreatment = metadata["pretreatment"], data_augmentation = metadata["data_augmentation"])
        log.info(f'POST /dataset/frames/ : Frame {files[0].filename} ajoutée avec succès au dataset {metadata["dataset"]}.')
        return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)
    
    except Exception as e :
        log.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e} ")




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
                return JSONResponse(content={"error": f"Le champ {i} ne peut pas être modifié."}, status_code=422)

        # possible de rajouter dataset id / data augmentation / test à set_img
        mg.update_frame(update["id"], update["query"])

        log.info(f'PUT /dataset/frames/ : Frame {update["id"]} modifiée avec succès.')
        return JSONResponse(content={"message": f"Frame {update['id']} modifiée avec succès"}, status_code=200)
    
    except Exception as e :
        log.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")
    

@app.delete("/dataset/frames/{id}")
async def delete_frame(mg : Annotated[Mongo, Depends(mongo_connect)], id: str):
    try : 
        if len(id) != 24 :
            mg.client.close()
            raise HTTPException(status_code=422, detail="ID must have 24-character hex string")

        response = mg.delete_frame(id)

        if response :
            mg.client.close()
            log.info(f'DELETE /dataset/frames/id : Frame {id} supprimée avec succès.')
            return JSONResponse(content={"message": "Élément supprimé avec succès"}, status_code=200)
        else :
            mg.client.close()
            raise HTTPException(status_code=422, detail="ID inexistant")
    
    except Exception as e : 
        log.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")

@app.post("/predict/")
async def predict(mg : Annotated[Mongo, Depends(mongo_connect)], files: list[UploadFile] = File(...)):
    try:
        img = files[0].file.read()

        img = mg.byte_to_img(img)

        # predict 
        model = Model()
        predict = model.predict_image(img, 0.5, 0.5)
        # res = predict.tojson()
        res = []
        for item in predict :
            res.append(item.tojson())
        #     img = item.plot()
        #     img = img.to_list()
        #     pred = {"img" : img,
        #             "names" : item.names,
        #             "boxes" : item.boxes.numpy()}
        #     res.append(pred)

        log.info(f'POST /predict/ : {files[0].filename} pred => {predict}.')
        return JSONResponse(content=res, status_code=200)
    
    except Exception as e :
        log.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e} ")