import logging
import os


if "log" not in os.listdir("src") :
    os.makedirs(os.path.join("src", "log"))
if "automatic_dataset.log" not in os.listdir(os.path.join("src", "log")):
    with open ("automatic_dataset.log", "w") as log_file:
        log_file.write("init log")

log = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8')
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s : %(filename)s:%(lineno)s - %(levelname)s >>> %(message)s'))
file_handler = logging.FileHandler(os.path.join("src","log",f"automatic_dataset.log"))
file_handler.setFormatter(logging.Formatter('%(asctime)s : %(filename)s:%(lineno)s - %(levelname)s >>> %(message)s'))
log.addHandler(console_handler)   
log.addHandler(file_handler)
