import io
import os 
import json

from PIL import Image, ImageDraw
import gradio as gr
import httpx

from ultralytics import YOLO

from config import *

headers = {"X-API-Key" : list(API_KEYS.keys())[0]}
model = YOLO(os.path.join("model", "yolov8n_custom201223_train9.pt"))


def predict_image(img):
    # Pil to byte
    imgbyte = io.BytesIO()
    img.save(imgbyte, format="png")
    imgbyte = imgbyte.getvalue()

    # export
    image = [("files", imgbyte)]
    response = httpx.post(f"http://traefik/api-ia/predict/", files = image, headers=headers, timeout=30.0)
    results = json.loads(response.content)
    draw = ImageDraw.Draw(img)
    # convert to image
    for r in results:
        r = json.loads(r)
        for i in r :
            x_min, y_min, x_max, y_max = i["box"]["x1"], i["box"]["y1"], i["box"]["x2"], i["box"]["y2"]
            name = i["name"]
            confidence = i["confidence"]
            text = str(name) + str(confidence)

            # Créer un objet ImageDraw pour dessiner sur l'image

            # Dessiner la boîte englobante
            draw.rectangle([x_min, y_min, x_max, y_max], width=2, outline='#C3F550')
            draw.text([x_min, y_min], text=text, font_size=26, stroke_width=1, fill="#C3F550")


    return img


iface = gr.Interface(
    fn=predict_image,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        # gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence threshold"),
        # gr.Slider(minimum=0, maximum=1, value=0.45, label="IoU threshold")
    ],
    outputs=gr.Image(type="pil", label="Result"),
    title="Ultralytics Gradio",
    description="Upload images for inference. The Ultralytics YOLOv8n model is used by default.",
)

if __name__ == '__main__':
    iface.launch(server_name="0.0.0.0")