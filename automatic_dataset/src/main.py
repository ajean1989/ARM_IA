"""
Lance la détection automatique sur le dossier "to_analyze" puis conserve les vidéos dans le dossier "analyzed".
"""

import os
import sys

from automatic_dataset_creation import automatic_dataset
from log import Logg

log = Logg()
log_debug = log.set_log_automatic_dataset_debug()

print(sys.path)

to_analyze_folder = os.path.join("src", "to_analyze")
analyzed_folder = os.path.join("src", "analyzed")

files_to_analyze = os.listdir(to_analyze_folder)

for file in files_to_analyze :
    log_debug.info(f"Analyse du fichier {file}")
    process = automatic_dataset(os.path.join("src", "to_analyze", file))
    process()
    
    # transfert du flux vidéo vers dossier "done".
    source_path = os.path.join(to_analyze_folder, file)
    destination_path = os.path.join(analyzed_folder, file)

    # Déplacer le fichier
    # os.rename(source_path, destination_path)
