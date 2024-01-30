from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Annotated
from app.mongo import Mongo
from app.maria import Maria
from config import API_KEYS




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
    dependencies=[Depends(validate_api_key)]
)

# Connexion Mongo DB
def mongo_connect():        # Permet d'overwrite pour les tests
    return Mongo(False)


# Connexion Maria DB
def maria_connect():        # Permet d'overwrite pour les tests
    return Maria(False)



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

        mg.set_img(files[0].file.read(), files[1].file.read(), dataset_id = metadata["dataset"], dataset_extraction = metadata["dataset_extraction"], pretreatment = metadata["pretreatment"], data_augmentation = metadata["data_augmentation"])
        
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
    
 








# Interact with Maria DB
    
## Item

class Item(BaseModel):
    id_code : str
    name: str
    brand : str
    ingredient : str
    allergen: str
    nutriment : str
    nutriscore : str
    ecoscore : str
    packaging: str
    image : str
    url_openfoodfact : str

@app.post("/items/")
async def record_item(mr : Annotated[Maria, Depends(maria_connect)], item: Item):
    try :
        item = item.model_dump()
        mr.create_item(id_code=item["id_code"], name=item["name"], brand=item["brand"], ingredient=item["ingredient"], allergen=item["allergen"], nutriment=item["nutriment"], nutriscore=item["nutriscore"], ecoscore=item["ecoscore"] , packaging=item["packaging"], image=item["image"], url_openfoodfact=item["url_openfoodfact"])
        return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")
    
@app.get("/items/")
async def get_items(mr : Annotated[Maria, Depends(maria_connect)]):
    try : 
        res = mr.get_item()
        res = [dict(row) for row in res]
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message} - {res} - {type(res)}")

@app.get("/items/{id}")
async def get_item(mr : Annotated[Maria, Depends(maria_connect)], id: int):
    try : 
        res = mr.get_item(id)
        res = [dict(row) for row in res]
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message} - {res} - {type(res)}")


@app.put("/items/")
async def update_item(mr : Annotated[Maria, Depends(maria_connect)], item: Item):
    try : 
        item = item.model_dump()
        res = mr.update_item(id_code=item["id_code"], name=item["name"], brand=item["brand"], ingredient=item["ingredient"], allergen=item["allergen"], nutriment=item["nutriment"], nutriscore=item["nutriscore"], ecoscore=item["ecoscore"] , packaging=item["packaging"], image=item["image"], url_openfoodfact=item["url_openfoodfact"])
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")

@app.delete("/items/{id}")
async def delete_item(mr : Annotated[Maria, Depends(maria_connect)], id: int | None):
    try : 
        res = mr.delete_item(id)
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")




## User
    
class User(BaseModel):
    username: str
    last_name : str
    first_name : str
    age: int
    gender : int


@app.post("/users/")
async def record_user(mr : Annotated[Maria, Depends(maria_connect)], user: User):
    try :
        user = user.model_dump()
        username = user["username"]
        first_name = user["first_name"]
        last_name = user["last_name"]
        age = user["age"]
        gender = user["gender"]
        res = mr.create_user(username=username, last_name=last_name, first_name=first_name, age=age, gender=gender)
        return JSONResponse(content={"message": "User ajouté avec succès", "result" : str(res)}, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")

@app.get("/users/")
async def get_users(mr : Annotated[Maria, Depends(maria_connect)]):
    try : 
        res = mr.get_user()
        res = [dict(row) for row in res]
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message} ")   

@app.get("/users/{id}")
async def get_user(mr : Annotated[Maria, Depends(maria_connect)], id : int):
    try : 
        res = mr.get_user(id)
        res = [dict(row) for row in res]
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")

@app.put("/users/{id}")
async def update_user(mr : Annotated[Maria, Depends(maria_connect)], id : int, user : User):
    try : 
        user = user.model_dump()
        username = user["username"]
        first_name = user["first_name"]
        last_name = user["first_name"]
        age = user["age"]
        gender = user["gender"]
        res = mr.update_user(id_user=id, username=username, last_name=last_name, first_name=first_name, age=age, gender=gender)
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")

@app.delete("/users/{id}")
async def delete_user(mr : Annotated[Maria, Depends(maria_connect)], id: int):
    try : 
        res = mr.delete_user(id)
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")








## Place

class Place(BaseModel):
    name: str
    adresse : str
    postcode : str
    city: str

@app.post("/places/")
async def record_place(mr : Annotated[Maria, Depends(maria_connect)], place: Place):
    try :
        place = place.model_dump()
        name = place["name"]
        adresse = place["adresse"]
        postcode = place["postcode"]
        city = place["city"]
        res = mr.create_place(name=name, adresse=adresse, postcode=postcode, city=city)
        return JSONResponse(content={"message": "Place ajoutée avec succès", "result" : str(res)}, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")

@app.get("/places/")
async def get_place(mr : Annotated[Maria, Depends(maria_connect)]):
    try : 
        res = mr.get_place()
        res = [dict(row) for row in res]
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message} ")   
    
@app.get("/places/{id}")
async def get_place(mr : Annotated[Maria, Depends(maria_connect)], id: int):
    try : 
        res = mr.get_place(id)
        res = [dict(row) for row in res]
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message} ")   

@app.put("/places/{id}")
async def update_place(mr : Annotated[Maria, Depends(maria_connect)], id: int, place : Place):
    try : 
        place = place.model_dump()
        name = place["name"]
        adresse = place["adresse"]
        postcode = place["postcode"]
        city = place["city"]
        res = mr.update_place(id_place = id, name=name, adresse=adresse, postcode=postcode, city=city)
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")

@app.delete("/places/{id}")
async def delete_place(mr : Annotated[Maria, Depends(maria_connect)], id: int):
    try : 
        res = mr.delete_place(id)
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")







## Scan
    
class Scan(BaseModel):
    id_user: int | None
    id_code : str | None
    id_place : int | None

@app.post("/scan/")
async def record_scan(mr : Annotated[Maria, Depends(maria_connect)], scan: Scan):
    try :
        scan = scan.model_dump()
        mr.create_scan(scan["id_user"], scan["id_code"], scan["id_place"], )
        return JSONResponse(content={"message": "Scan ajoutée avec succès"}, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")


@app.get("/scan/")
async def get_scan(mr : Annotated[Maria, Depends(maria_connect)], id_user : int | None = None):
    try :
        if id_user == None :
            res = mr.get_scan()
        else : 
            res = mr.get_scan(id_user)
        res = [dict(row) for row in res]
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")

@app.delete("/scan/")
async def delete_scan(mr : Annotated[Maria, Depends(maria_connect)], id: int):
    try : 
        res = mr.delete_scan(id)
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = str(e)
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")