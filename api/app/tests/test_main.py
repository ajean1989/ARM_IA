import os
import json
from time import time

from fastapi.testclient import TestClient
from bson.objectid import ObjectId

from app.main import app, mongo_connect
from app.mongo import Mongo
from app.config import API_KEYS

from app.log import Logg
from app.model import Model

# Log

log = Logg()
log_debug = log.set_log_api_ia_debug()


client = TestClient(app)

def override_mongo():
    return Mongo(True)


app.dependency_overrides[mongo_connect] = override_mongo


headers = {'X-API-Key': list(API_KEYS.keys())[0]}



def test_api_key():

    response = client.get("/")
    assert response.status_code == 403

    response = client.get("/", headers=headers)
    assert response.status_code == 200

    assert response.json() == {"Hello": "World"}
    



def test_get_dataset(binary_annotation, binary_metadata, binary_annotation_1):

    mongo = Mongo(test = True)

    # Ajout de 2 frames
    
    mongo.reset_db()
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]
    response1 = client.post("/dataset/frames/", files = files, headers=headers)

    assert response1.status_code == 200

    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation_1), ("files" , binary_metadata)]
    response2 = client.post("/dataset/frames/", files = files, headers=headers)

    assert response2.status_code == 200

    # Téléchargement
    response = client.get("/dataset/0", headers=headers)
    assert response.status_code == 200

    # Récupérer le zip
    print(response)
    with open(os.path.join("app","dataset_0.zip"), "wb") as zip:
        zip.write(response.content)

    assert "dataset_0.zip" in os.listdir("app")

    # Supprimer le zip
    os.remove(os.path.join("app","dataset_0.zip"))
    assert "dataset_0.zip" not in os.listdir("app")

    # Supprimer le contenu de temp
    mongo.remove_temp_get_dataset()

    mongo.client.close()



def test_add_frame(binary_annotation, binary_metadata):

    mongo = Mongo(test = True)

    # Ajout d'un frame
    
    mongo.reset_db()
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]
    response = client.post("/dataset/frames/", files = files, headers=headers)

    assert response.status_code == 200

    # Image n'est pas un jpg, png, etc. 
    mongo.reset_db()
    img = open("app/tests/sample/test.txt","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]
    response = client.post("/dataset/frames/", files = files, headers=headers)

    assert response.status_code == 422

    # Array n'a pas 3 éléments
    mongo.reset_db()
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation)]
    response = client.post("/dataset/frames/", files = files, headers=headers)

    assert response.status_code == 422
    assert response.json() == {"error": "array must have 3 binaries elements"}

    mongo.client.close()

def test_add_frame_with_json(binary_img, dict_annotation, dict_metadata):
    img = open("app/tests/sample/img_1.png","rb")
    image = ('files', img)
    
    binary_anotation = []
    binary_anotation.append(dict_annotation)
    binary_anotation = json.dumps(binary_anotation)
    binary_anotation = str(binary_anotation) # transform le jsonObject en str
    binary_anotation = bytes(binary_anotation, "utf-8")
    anotations = ("files", binary_anotation)

    metadata = json.dumps(dict_metadata)
    metadata = str(metadata) # transform le jsonObject en str
    metadata = bytes(metadata, "utf-8")
    metadatas = ("files", metadata)

    frame = [image, anotations, metadatas]

    print(frame)

    response = client.post("/dataset/frames/", files = frame, headers=headers)
    print(response.content)
    assert response.status_code == 200




def test_update_frame(binary_annotation, binary_metadata):

    mongo = Mongo(test = True)

    # Ajout d'un frame
    mongo.reset_db()
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]


    response = client.post("/dataset/frames/", files = files, headers=headers)
    assert response.status_code == 200

    res = mongo.dataset_collection.find_one({})
    assert res["data_augmentation"] == False 

    # Modification de data_augmentation
    id_init = (res["_id"]) 
    id = str(res["_id"]) 
    pp = ObjectId(id)
    assert id_init == pp 

    update = {
        "id" : id,
        "query" : {"data_augmentation" : True},
        "test" : True
    }

    response = client.put("/dataset/frames/", json = update, headers=headers)
    assert response.status_code == 200

    res_updated = mongo.dataset_collection.find_one({"_id": id_init})
    assert res_updated["data_augmentation"] == True 

    # Multi modification

    update = {
        "id" : id,
        "query" : {"data_augmentation" : True,
                   "pre_treatment" : True},
        "test" : True
    }

    response = client.put("/dataset/frames/", json = update, headers=headers)
    assert response.status_code == 200

    res_updated = mongo.dataset_collection.find_one({"_id": id_init})
    assert res_updated["data_augmentation"] == True 
    assert res_updated["pre_treatment"] == True 


    # Cas où le champ de query n'existe pas

    update = {
        "id" : id,
        "query" : {"data_augment" : True},
        "test" : True
    }

    response = client.put("/dataset/frames/", json = update, headers=headers)
    assert response.status_code == 422

    mongo.client.close()


def test_delete_frame(binary_annotation, binary_metadata):

    mongo = Mongo(test = True)

    # Ajout d'un frame
    mongo.reset_db()
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]
    response = client.post("/dataset/frames/", files = files, headers=headers)

    assert response.status_code == 200

    # Suprression 
    res = mongo.dataset_collection.find_one({})

    nb =  mongo.dataset_collection.count_documents({})
    assert nb == 1

    id = res["_id"]
    response = client.delete(f"/dataset/frames/{id}", headers=headers)

    nb =  mongo.dataset_collection.count_documents({})

    assert nb == 0
    assert response.status_code == 200


    # Bad id 

    response = client.delete(f"/dataset/frames/000111125478541154555255", headers=headers)
    assert response.status_code == 422

    response = client.delete(f"/dataset/frames/00011", headers=headers)
    assert response.status_code == 422

    mongo.client.close()



def test_predict() : 
    img = open("app/tests/sample/img_1.png","rb")
    image = [('files', img)]
    response = client.post("/predict/", files=image, headers=headers)
    pred = json.loads(response.content)
    assert response.status_code == 200
    log_debug.debug(f"predddd : {type(pred), pred}")
    print(pred)
    assert len(pred) == 1
    for i in pred :
        i = json.loads(i)
        log_debug.debug(f"pppppred : {type(i), i}")
        # json.loads(i)
        # print(i["boxes"])
        # print(i["names"])

