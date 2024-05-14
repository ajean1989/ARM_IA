
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import httpx
import json
import re

from random import randint
import pandas as pd

from PIL import Image
from ultralytics import YOLO
import cv2
from pyzbar.pyzbar import decode

from src.config import *
from src.utils import Utils
from src.log import log


class automatic_dataset : 

    def __init__(self,input, test = True) :
        self.input = input
        self.weight = os.listdir(os.path.join("src", "model"))[0]
        self.model = YOLO(os.path.join("src", "model", self.weight))
        self.tracker = os.path.join("src","tracker", "custom_botsort.yaml")
        # self.tracker = "tracker/bytetrack.yaml"
        self.detected = pd.DataFrame(columns=["name","id","bbxyxy","bbxywhn","code"])
        # Dossier temp nécéssaire pour faire la detection et suppr img sans détection
        self.path_temp = os.path.join("src", "temp")
        # self.path_dataset = os.path.join("backend","datasets","bottle_dataset","dataset")
        self.test = test
        # self.adresse_mongo = adresse_mongo
        # self.adresse_maria= adresse_maria
        self.headers = {"X-API-Key" : list(API_KEYS.keys())[0]}
        self.dataset_ids = [0,1]
        if re.search("oiv7", self.weight):
            self.classes = [199,171,62,57,535]
        else : 
            # pre trained model
            self.classes = [39,41]
        if re.search("train", self.weight):
            #custom model
            self.classes = [0]

      

    def __call__(self, vizualize= False, max_frame = -1):
        self.reset_temp()
        self.detection(vizualize, max_frame)
        self.code()
        self.reset_temp()


    def reset_temp(self) :
        """ Supprime tous les fichiers temp"""

        temp = os.listdir(self.path_temp)
        for img in temp: 
            os.remove(os.path.join(self.path_temp,img))
        
        log.info("temp files deleted.")
        



    
    def detection(self, vizualize= False, max_frame = -1) :

        """ 
        Détection d'objets "bottle" et "cup" (COCO) 
        || "Bottle", "Box", "Tin can" (OIV7) au sein d'un flux video
        || "Object" dans le custom model

        Les frames avec détection sont placées dans temp/, dossier nécéssaire pour faire la detection et suppr img sans détection
        """

        # Supprimer temp
        self.reset_temp()

        frame_count, detection_count, id_count = 0, 0, 0

        cap = cv2.VideoCapture(self.input)

        while cap.isOpened():

            # Read a frame from the video
            success, frame = cap.read()
            # if frame_count%5 == 0 :
            if success:

                    # Run YOLOv8 inference on the frame
                    results = self.model.track(frame, persist=True, classes = self.classes , conf=0.1, tracker=self.tracker)
                    result = results[0]
                    
                    for r in result :
                        detection_count += 1
                        if r.boxes.id != None :
                            id_count += 1
                            print("x1, y1, x2, y2, id , conf, cls = ", r.boxes.data.tolist())
                            print('---')
                            print("id = ", r.boxes.id.int().cpu().tolist())
                            print('---')
                            print("class = ", r.boxes.cls)
                            print('---')
                        else : 
                            continue
                        
                        if vizualize :
                            # Visualize the results on the frame when id
                            annotated_frame = results[0].plot()
                            im = Image.fromarray(annotated_frame[..., ::-1])  # RGB PIL image
                            im.show()

                        # enregistrer l'image dans temp formaté : timestamp+randint(1024)
                        name = f"img_{str(int(time.time()))}_{randint(0,1023)}.png"
                        path = os.path.join(self.path_temp,name)
                        Image.fromarray(frame[:,:,::-1]).save(path,'PNG')

                        # !!!! une ligne par id dans le df self.detected pour la détection de plusieurs objets sur une image !!!
                        # Cela garde une trace (dict["nom","id","bb","code"]) du nom des fichiers + ID + bb enregristrés pour ajouter le label par la suite ou effacer
                        id = r.boxes.id.int().cpu().tolist()[0]
                        bbxyxy = r.boxes.xyxy[0].cpu().numpy() #[x1,y1,x2,y2]
                        bbxywhn = r.boxes.xywhn[0].cpu().numpy() #[x1,y1,x2,y2]

                        self.detected.loc[len(self.detected)] = [name, id, bbxyxy, bbxywhn, 0]
                        
            else:
                # Break the loop if the end of the video is reached
               break

            frame_count += 1

            if frame_count != -1 and frame_count == max_frame:
                break

        cap.release()
        cv2.destroyAllWindows()

        log.info(f"{frame_count} image(s) analysed")
        log.info(f"{detection_count} detected object(s)")
        log.info(f"{id_count} id(s) affected")
        # log.info(f"different(s( object(s) detected)) : {len(id)}")


    ## Faire une detection code sur les images temp, sur bb

    def code(self) :

        """ Détectection du code barre sur les objets détectés dans le dossier temp """

        for index, value in self.detected.iterrows():
            # ouvrir image
            
            with Image.open(os.path.join(self.path_temp,value["name"])) as image :
            # image = Image.open(os.path.join(self.path_temp,value["name"]))
            
                # cropper avec bb 
                image = image.crop(tuple(value["bbxyxy"]))

                # détection code 
                # img_crop.show()
                res_barcode = decode(image)
                if len(res_barcode) != 0 :
                    # propagation code à detected
                    # img_crop.show()
                    self.detected["code"].loc[self.detected["id"]==value["id"]] = res_barcode[0].data
                    log.info(f"code detected : {res_barcode[0].data} sur l'image {value['name']}")
            

        print(self.detected)

        # Transformer le dict en fichier text d'annotation yolo et enregistrer en bdd
        utils = Utils()
        frames = utils.pproc_frame(self.detected)
        print(frames)

        for frame in frames : 
            log.debug(f"files envoyé à l'API via POST: {frame}")


            #res = httpx.post(f"http://traefik/api-ia/dataset/frames/", files = frame, headers=self.headers)
            res = httpx.post(f"http://localhost/api-ia/dataset/frames/", files = frame, headers=self.headers)

            log.info(f" Réponse de l'API : {res.status_code} : {res.content}")
        
        return

     

    
    
    def retrieve_off(self, code : str) :
        """
        Scrap API openfoodfact à partir du code pour envoyer au datawarehouse.
        Récupère les informations utiles et les retourne dans un dictionnaire.
        """
        # API OFF
        result = httpx.get(f"https://world.openfoodfacts.org/api/v2/product/{code}.json")

        result = json.loads(result.text)

        utils_keys = ["_id", "allergens_tags","brands_tags","abbreviated_product_name_fr","ingredients_tags","nutriments","nutrition_grades_tags","ecoscore_tags","image_url","origins_tags","packaging_materials_tags"]

        drop_keys = []

        for key, value in result["product"].items() : 
            if key not in utils_keys :
                drop_keys.append(key)
        
        for i in drop_keys:
            result["product"].pop(i, None)

        # Product est la clé qui contient toutes les informations
        # Mapping des clés 
        data = {}
        data["id_code"] = str(result["product"]["_id"])
        data["brand"] = str(result["product"]["brands_tags"])
        data["name"] = str(result["product"]["abbreviated_product_name_fr"])
        data["ingredient"] = str(result["product"]["ingredients_tags"])
        data["allergen"] = str(result["product"]["allergens_tags"])
        data["nutriment"] = str(result["product"]["nutriments"])
        data["nutriscore"] = str(result["product"]["nutrition_grades_tags"])
        data["ecoscore"] = str(result["product"]["ecoscore_tags"])
        data["packaging"] = str(result["product"]["packaging_materials_tags"])
        data["image"] = str(result["product"]["image_url"])
        data["url_openfoodfact"] = f"https://fr.openfoodfacts.org/produit/{code}/"

        log.info(f"Données récupérée de l'API OpenFoodFact : {type(data)}\n {data}")


        # Envoie les données à l'api-backend
        # res = httpx.post(f"http://traefik/api-backend/items/", json=data, headers=self.headers)
        res = httpx.post(f"http://localhost/api-backend/items/", json=data, headers=self.headers)
        print('---')
        print(res.content)
        log.info(f" Réponse de l'API IA : {res.status_code} : {res.content}")


        return res

            




if __name__ == "__main__":
    create = automatic_dataset("data/sample/video_test_2.mp4", "yolov8n_custom201223_train9.pt")
    create()
    # create.api_off("3307130802557")