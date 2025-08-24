import os
import json
import torch
from dotenv import load_dotenv
from .model import build_model

_LABELS = None
_MODEL = None 
_DEVICE = None

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
   config = get_config()
   num_classes = len(get_labels())
   model = build_model(num_classes)
   load_state = torch.load(config["model_path"], map_location=config["device"])
   model.load_state_dict(load_state) 
   model.to(config["device"])
   model.eval()
   return model

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = load_model()
    return _MODEL
        


def get_labels():
    global = _LABELS
    if _LABELS is None:
        config = get_config()
        with open(config["labels_path"]) as file:
            _LABELS = json.load(file)
        return _LABELS
    return _LABELS