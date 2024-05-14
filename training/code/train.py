import mlflow
from ultralytics import YOLO

# Load a pretrained YOLO model (recommended for training)
model = YOLO('yolov8n.pt')

# Train the model using the 'coco128.yaml' dataset for 3 epochs
results = model.train(data='coco128.yaml', epochs=3)

# Evaluate the model's performance on the validation set
results = model.val()

# Export the model to ONNX format
success = model.export(format='onnx')

with mlflow.start_run():

    mlflow.autolog()

    # Set tracking server
    mlflow.set_tracking_uri(uri="http://localhost:5000")

    # Experiment
    mlflow.set_experiment("Code model")