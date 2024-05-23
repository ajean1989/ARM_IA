import os
import mlflow
from ultralytics import YOLO


if __name__ == "__main__":

    # Set tracking server
    mlflow.set_tracking_uri(uri="https://jacquenet.com")
    print("URI du serveur de suivi MLflow :", mlflow.get_tracking_uri())

    mlflow.set_experiment("Test")
    print("Expérience actuelle MLflow :", mlflow.get_experiment_by_name("Test"))

    

    with mlflow.start_run():

        mlflow.autolog()

        # Load a pretrained YOLO model (recommended for training)
        model = YOLO('yolov8n.pt')

        # Train the model using the 'coco128.yaml' dataset for 3 epochs
        results = model.train(data=os.path.join("code", 'test_dataset.yml'), epochs=1, batch=-1, device='0')

        # Evaluate the model's performance on the validation set
        results = model.val()

        # Export the model to ONNX format
        success = model.export(format='onnx')