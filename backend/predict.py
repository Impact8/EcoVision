from typing import Tuple, List
import torch
from backend.load import get_config, get_labels, get_model
from util import load_tensor_for_model

config = get_config()
labels = get_labels()
model = get_model()
model.eval()

def predict(img_file, topk: int = 1):

    tensor = load_tensor_for_model(img_file)
    tensor = tensor.to(config["device"])

    with torch.no_grad():
        model_output = model(tensor)
        probs = torch.softmax(model_output, 1)
        probs = probs.squeeze(0)

        topk = max(1, min(topk, len(labels)))
        top_probs, top_indexes = torch.topk(probs, topk)
        results = [(labels[i], float(c)) for c, i in zip(top_probs, top_indexes)]
        return results




    

