import os

from PIL import Image
from ultralytics import YOLO


class Model :
    def __init__(self) -> None:
        path = os.path.join("app", "model", "yolov8n_custom201223_train9.pt")
        self.model = YOLO(path)
    
    def predict_image(self, img, conf_threshold, iou_threshold):
        results = self.model.predict(
            source=img,
            conf=conf_threshold,
            iou=iou_threshold,
            show_labels=True,
            show_conf=True,
            imgsz=640,
        )

        return results
