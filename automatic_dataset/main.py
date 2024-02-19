import os
import shutil

from automatic_dataset.automatic_dataset_creation import automatic_dataset

to_analyze_folder = os.path.join("automatic_dataset", "to_analayze")
analyzed_folder = os.path.join("automatic_dataset", "analayzed")

for file in to_analyze_folder :
    process = automatic_dataset(file)
    process()
    
    # transfert du fluw vidéo vers dossier "done".
    source_path = os.path.join(to_analyze_folder, file)
    destination_path = os.path.join(analyzed_folder, file)
    shutil.copy(source_path, destination_path)