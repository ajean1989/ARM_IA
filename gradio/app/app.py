import io

import PIL.Image as Image
import gradio as gr
import httpx

from ultralytics import ASSETS, YOLO

from config import *

headers = {"X-API-Key" : list(API_KEYS.keys())[0]}
model = YOLO("yolov8n_custom201223_train9.pt")


def predict_image(img):
    # Pil to byte
    imgbyte = io.BytesIO()
    img.save(imgbyte, format="png")
    imgbyte = imgbyte.getvalue()

    # export
    image = [("files", imgbyte)]
    results = httpx.post(f"http://localhost/api-ia/dataset/frames/", files = image, headers=headers)

    # convert to image
    for r in results:
        im_array = r.plot()
        im = Image.fromarray(im_array[..., ::-1])

    return im


iface = gr.Interface(
    fn=predict_image,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence threshold"),
        gr.Slider(minimum=0, maximum=1, value=0.45, label="IoU threshold")
    ],
    outputs=gr.Image(type="pil", label="Result"),
    title="Ultralytics Gradio",
    description="Upload images for inference. The Ultralytics YOLOv8n model is used by default.",
    examples=[
        [ASSETS / "bus.jpg", 0.25, 0.45],
        [ASSETS / "zidane.jpg", 0.25, 0.45],
    ]
)

if __name__ == '__main__':
    iface.launch(share=True)