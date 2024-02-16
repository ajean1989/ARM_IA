from PIL import Image
import io
import os
import logging
import datetime
import json


class Utils :

    log = logging.getLogger("log-auto")
    log.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    log.addHandler(console_handler)   
    log.addHandler(file_handler)   

    def __init__(self) -> None:
        self.pretreatment = 1

    def img_to_byte(self, img):
        """ Convertion d'une image PIL en BYTES """
        imgbyte = io.BytesIO()
        img.save(imgbyte, format="png")
        imgbyte = imgbyte.getvalue()
        return imgbyte
    
    def byte_to_img(self, imgbyte):
        """ Conversion des BYTES en image PIL"""
        imgbyte_io = io.BytesIO(imgbyte)
        image_pil = Image.open(imgbyte_io)
        return image_pil

    def set_img(self,img, txt_path, dataset_id = 0, data_augmentation = False, test = True):
        """ Enregistre les images qui on eu une détection et les métadonnées :
        Date de la mise en base
        Code + BB
        Nom du dataset : 0 = all
        pré-traitement y a-t-il eu 
        Data augmentation y a-t-il eu
        """

        imgbyte = self.img_to_byte(img)

        # Création du document
        new_document = {}

        new_document["img"] = imgbyte
        new_document["date"] = datetime.datetime.today()

        with open (f"{txt_path}", "r") as txt :
            rows = txt.readlines()
            for index, row in enumerate(rows) :
                words = row.split()
                new_document[f"label_{index}"] = {"code" : words[0], "bb" : [words[1], words[2], words[3], words[4]]}
        new_document["dataset"] = dataset_id
        new_document["pretreatment"] = self.pretreatment
        new_document["data_augmentation"] = data_augmentation

        doc = json.dumps(new_document)

        # Insertion en base
        # if test :
        #     self.dataset_test_collection.insert_one(new_document)
        # else : 
        #     self.dataset_collection.insert_one(new_document)
        return doc
    
    def pproc_frame(self, detected_df, dataset_id = 0, dataset_extraction = "ARM", pretreatment = False, data_augmentation = False, test = True):
        """ 
        Mise en forme des données d'une frame pour envoie à la bdd mongo via api-ia.
        Add a new frame with an array of binaries [image, annotation, metadata] in dataset collection.
        
        * [("files",(open(img_path,'rb'), ("files",annotation),("files",metadata)]
        
        * annotation = b'[{
            "label" : "Object",
            "label_int" : 0,
            "bounding box" : [0.11212, 0.11, 0.4564, 0.4546]
        },
        {
            "label" : "bla",
            "label_int" : 2,
            "bounding box" : [0.11, 0.11, 0.45, 0.45]
        }]'

        * metadata = b'{
            "dataset_id" : 0, 
            "dataset_extraction" : "ARM", 
            "pretreatment" : False, 
            "data_augmentation" : False, 
            "test" : True}'

        """

        # Garde les détections
        code_detected = detected_df[detected_df["code"] != 0]

        # Liste qui contient chaque frame
        frames = []

        # Création de la liste d'anotation : rassemble plusieurs lignes de code_detected dans une liste.
        names = set(code_detected["name"])
        for name in names :
            data = code_detected[code_detected["name"]==name]
            image = (name, open(os.path.join("automatic_dataset", "temp", name),"rb"))

            binary_anotation = []
            for index, value in data.iterrows(): 
                #transformer en dict
                object_anotation = {"label" : "undefined",
                                    "label_int" : str(value["code"])[2:-1],
                                    "bounding_box" : [str(value["bbxywhn"][0]), str(value["bbxywhn"][1]), str(value["bbxywhn"][2]), str(value["bbxywhn"][3])]}
                binary_anotation.append(object_anotation)
            binary_anotation = bytes().join(bytes([x]) for x in binary_anotation)
            anotations = (name, binary_anotation)

            metadata = f'{"dataset_id" : {dataset_id}, "dataset_extraction" : {dataset_extraction}, "pretreatment" : {pretreatment}, "data_augmentation" : {data_augmentation}, "test" : {test}}'
            metadata = bytes(metadata)
            metadatas = (name, metadata)
            frames.append([image, anotations, metadatas])
        
        return frames

