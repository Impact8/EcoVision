import os
import json
import torch
from dotenv import load_dotenv

_LABELS = None

load_dotenv()

def get_device(device: str = "cpu"):
    if device == "cuda" and torch.cuda.is_available():
        return "cuda"
    elif device == "mps" and torch.mps.is_available():
        return "mps"
    else: 
        return "cpu"



def get_config():
    model_path = os.getenv("MODEL_PATH")
    labels_path = os.getenv("LABELS_PATH")
    device = os.getenv("DEVICE", "CPU").lower()
    
    return {
        "model_path": model_path,
        "labels_path": labels_path,
        "device": get_device(device)
    }


def load_model():
   pass

def get_model():
    pass


def get_labels():
    if _LABELS is None:
        config = get_config()
        with open(config["labels_path"]) as file:
            _LABELS = json.load(file)
        return _LABELS