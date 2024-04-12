import logging
import os

class Logg : 
    def __init__(self) -> None:
        pass

    def set_log_automatic_dataset_debug(self):
        log_automatic_debug = logging.getLogger("automatic-dataset-debug")
        log_automatic_debug.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        file_handler = logging.FileHandler(os.path.join("src","log","automatic-dataset-debug.log"))
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        log_automatic_debug.addHandler(console_handler)   
        log_automatic_debug.addHandler(file_handler)
        return  log_automatic_debug
    
    def set_log_automatic_dataset_info(self):
        log_automatic_info = logging.getLogger("automatic-dataset-info")
        log_automatic_info.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        file_handler = logging.FileHandler(os.path.join("src","log","automatic-dataset-info.log"))
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        log_automatic_info.addHandler(console_handler)   
        log_automatic_info.addHandler(file_handler)
        return  log_automatic_info
    