from ultralytics import YOLO
import settings

def load_model(model_path):
    """
    Load YOLO model dari path yang ditentukan.
    """
    return YOLO(model_path)
