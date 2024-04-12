import io
import os
import json

from PIL import Image

from src.log import Logg


class Utils :  

    def __init__(self) -> None:
        self.pretreatment = 1
        log = Logg()
        self.log_debug = log.set_log_automatic_dataset_debug()


    def img_to_byte(self, img):
        """ Convertion d'une image PIL en BYTES """
        try : 
            imgbyte = io.BytesIO()
            img.save(imgbyte, format="png")
            imgbyte = imgbyte.getvalue()
            return imgbyte
        except : 
            self.log_debug.error(Exception)
    
    def byte_to_img(self, imgbyte):
        """ Conversion des BYTES en image PIL"""
        try : 
            imgbyte_io = io.BytesIO(imgbyte)
            image_pil = Image.open(imgbyte_io)
            return image_pil
        except :
            self.log_debug.error(Exception)

    # def set_img(self,img, txt_path, dataset_id = 0, data_augmentation = False):
        # """ 
        # Enregistre les images qui on eu une détection et les métadonnées :
        # Date de la mise en base
        # Code + BB
        # Nom du dataset : 0 = all
        # pré-traitement y a-t-il eu 
        # Data augmentation y a-t-il eu
        # """

        # imgbyte = self.img_to_byte(img)

        # # Création du document
        # new_document = {}

        # new_document["img"] = imgbyte
        # new_document["date"] = datetime.datetime.today()

        # with open (f"{txt_path}", "r") as txt :
        #     rows = txt.readlines()
        #     for index, row in enumerate(rows) :
        #         words = row.split()
        #         new_document[f"label_{index}"] = {"code" : words[0], "bb" : [words[1], words[2], words[3], words[4]]}
        # new_document["dataset"] = dataset_id
        # new_document["pretreatment"] = self.pretreatment
        # new_document["data_augmentation"] = data_augmentation

        # doc = json.dumps(new_document)

        # return doc
    
    def pproc_frame(self, detected_df, dataset_id = [0], dataset_extraction = "ARM", pretreatment = False, data_augmentation = False, test = True):
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
            "dataset_id" : [0], 
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
            image = ("files", open(os.path.join("src", "temp", name),"rb"))

            binary_anotation = []
            for index, value in data.iterrows(): 
                #transformer en dict
                object_anotation = {"label" : "undefined",
                                    "label_int" : int(str(value["code"])[2:-1]),
                                    "bounding box" : [float(value["bbxywhn"][0]), float(value["bbxywhn"][1]), float(value["bbxywhn"][2]), float(value["bbxywhn"][3])]}
           
                binary_anotation.append(object_anotation)
            binary_anotation = json.dumps(binary_anotation)
            binary_anotation = str(binary_anotation) # transform le jsonObject en str
            binary_anotation = bytes(binary_anotation, "utf-8")
            anotations = ("files", binary_anotation)

            metadata = {"dataset" : dataset_id, 
                        "dataset_extraction" : dataset_extraction, 
                        "pretreatment" : pretreatment, 
                        "data_augmentation" : data_augmentation, 
                        "test" : test} 
            metadata = json.dumps(metadata)
            metadata = str(metadata) # transform le jsonObject en str
            metadata = bytes(metadata, "utf-8")
            metadatas = ("files", metadata)
            frames.append([image, anotations, metadatas])
        return frames

