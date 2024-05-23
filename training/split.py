""" Programme permettant de split corretement le dataset pour l'entrainement."""

import os 
import random
import shutil
import yaml
import json

def split(dataset_name, part_val, part_test) : 
    """
    Cette fonction prend le dataset brut dans le dossier 'raw', et le split pour l'entrainement pour le déplacer dans le dossier 'ready'.
    dataset_name = nom du dossier dans /data/raw/.
    """

    # vérfiie que le dossier existe bien
    try :
        if dataset_name in os.listdir(os.path.join("data", "ready")) :
            pass
        else : 
            raise(f"{dataset_name} n'est pas dans le dossier /data/ready.")
    except Exception as e:
        print(e)




    # Création des dossers dans /data/ready

    if dataset_name not in os.listdir(os.path.join("data", "ready")) : 
        os.makedirs(os.path.join("data", "ready", dataset_name))
        os.makedirs(os.path.join("data", "ready", dataset_name, "images"))
        os.makedirs(os.path.join("data", "ready", dataset_name, "images", "train"))
        os.makedirs(os.path.join("data", "ready", dataset_name, "images", "val"))
        os.makedirs(os.path.join("data", "ready", dataset_name, "images", "test"))
        os.makedirs(os.path.join("data", "ready", dataset_name, "labels"))
        os.makedirs(os.path.join("data", "ready", dataset_name, "labels", "train"))
        os.makedirs(os.path.join("data", "ready", dataset_name, "labels", "val"))
        os.makedirs(os.path.join("data", "ready", dataset_name, "labels", "test"))
    # Parcours de dossier du dataset dans "raw"

    raw_dataset = os.listdir(os.path.join("data", "raw", dataset_name))
    raw_dataset = [i[:-4] for i in raw_dataset if i[:-4] != ".txt"]
    random.shuffle(raw_dataset)

    element_no = len(raw_dataset) 
    
    for index, file in enumerate(raw_dataset) : 
        if index < element_no * part_test :
            shutil.copy(os.path.join("data", "raw", dataset_name, f"{file}.png"), os.path.join("data", "ready", dataset_name, "images", "val", f"{file}.png"))
            shutil.copy(os.path.join("data", "raw", dataset_name, f"{file}.txt"), os.path.join("data", "ready", dataset_name, "labels", "val", f"{file}.txt"))
        elif (index >= element_no * part_test)  and (index < element_no * (part_test + part_val)) : 
            shutil.copy(os.path.join("data", "raw", dataset_name, f"{file}.png"), os.path.join("data", "ready", dataset_name, "images", "test", f"{file}.png"))
            shutil.copy(os.path.join("data", "raw", dataset_name, f"{file}.txt"), os.path.join("data", "ready", dataset_name, "labels", "test", f"{file}.txt"))
        else : 
            shutil.copy(os.path.join("data", "raw", dataset_name, f"{file}.png"), os.path.join("data", "ready", dataset_name, "images", "train", f"{file}.png"))
            shutil.copy(os.path.join("data", "raw", dataset_name, f"{file}.txt"), os.path.join("data", "ready", dataset_name, "labels", "train", f"{file}.txt"))



    # Vérification 
    len_images_val = len(os.listdir(os.path.join("data", "ready", dataset_name, "images", "val",)))
    len_images_test = len(os.listdir(os.path.join("data", "ready", dataset_name, "images", "test",)))
    len_images_train = len(os.listdir(os.path.join("data", "ready", dataset_name, "images", "train",)))

    len_labels_val = len(os.listdir(os.path.join("data", "ready", dataset_name, "labels", "val",)))
    len_labels_test = len(os.listdir(os.path.join("data", "ready", dataset_name, "labels", "test",)))
    len_labels_train = len(os.listdir(os.path.join("data", "ready", dataset_name, "labels", "train",)))

    print(f"{len_images_val} ({len_images_val/element_no}%) images de validations dans le dossier ready.")
    print(f"{len_images_test} ({len_images_test/element_no}%) images de test dans le dossier ready.")
    print(f"{len_images_train} ({len_images_train/element_no}%) images de train dans le dossier ready.")

    print(f"{len_labels_val} ({len_labels_val/element_no}%) labels de validations dans le dossier ready.")
    print(f"{len_labels_test} ({len_labels_test/element_no}%) labels de test dans le dossier ready.")
    print(f"{len_labels_train} ({len_labels_train/element_no}%) labels de train dans le dossier ready.")

def generate_yml(dataset_name) : 
    """ Génère le fichier yml à passer à YOLO pour l'entrainement. """

    # Récupération des classes des fichiers txt
    labels = set()

    val_folder = os.path.join("data", "ready", dataset_name, "labels", "val")
    test_folder = os.path.join("data", "ready", dataset_name, "labels", "test")
    train_folder = os.path.join("data", "ready", dataset_name, "labels", "train")


    fold1 = ["train", "test", "val"]
    
    for i in fold1 :
        folder =  os.path.join("data", "ready", dataset_name, "labels", i)
        for j in os.listdir(folder):
            with open(os.path.join("data", "ready", dataset_name, "labels", i, j), 'r', encoding="utf8") as file:
                # Parcourir chaque ligne du fichier
                for line in file:
                    # Séparer la ligne en mots
                    words = line.split()
                    # Vérifier si la ligne n'est pas vide et afficher le premier mot
                    if words:
                        labels.add(words[0])

    # Contenu du fichier YAML

    
    yml_data = {
        'path': 'C:\Users\Adrien\Desktop\ARM\ARM_IA\training\data\ready\test_dataset',
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'names': {}
    }

    for index, i in enumerate(list(labels)):
        yml_data['names'][int(index)] = i

    # Chemin du fichier à créer
    file_path = os.path.join("code", f'{dataset_name}.yml')

    # Écriture du fichier YAML
    with open(file_path, 'w') as file:
        yaml.dump(yml_data, file, default_flow_style=False)

    print(f"Le fichier {file_path} a été créé avec succès.")


    # Modification de la classe de chaque fichier label pour lui appliquer la clé de la liste labels

    for i in fold1 :
        folder =  os.path.join("data", "ready", dataset_name, "labels", i)
        for j in os.listdir(folder):
            with open(os.path.join("data", "ready", dataset_name, "labels", i, j), 'r', encoding="utf8") as file:
                # Parcourir chaque ligne du fichier
                for line in file:
                    # Séparer la ligne en mots
                    words = line.split()
                    # Vérifier si la ligne n'est pas vide et afficher le premier mot
            with open(os.path.join("data", "ready", dataset_name, "labels", i, j), 'w', encoding="utf8") as file:
                index = list(labels).index(words[0])
                file.write(f"{index} {words[1]} {words[2]} {words[3]} {words[4]}")


split("test_dataset", 0.1, 0.1)


generate_yml("test_dataset")

# def put_labels_dictionary(label):

#     with open("labels_dictionary.json", 'a') as labels :
#         data = json.loads(labels.reads())
#         if label not in data.values() : 
#             data[max(int(data.keys()))+1] = label



