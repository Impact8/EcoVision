import io
from typing import Tuple, List
import torch
from PIL import Image
import torchvision.transforms as T 
from backend.load import get_config, get_labels, get_model

    

transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
    ) 
])

def process_img(img_file):
    if isinstance(img_file, bytes):
        bytes_img = io.BytesIO(img_file)
        image = Image.open(bytes_img)
    else:
        image = Image.open(img_file)

    image = image.convert("RGB")
    tensor = transform(image)
    tensor = tensor.unsqueeze(0)
    return tensor

def predict(img_file, topk: int = 1):
    config = get_config()
    labels = get_labels()
    model = get_model()

    tensor = process_img(img_file)
    tensor = tensor.to(config["device"])

    with torch.no_grad():
        model_output = model(tensor)
        probs = torch.softmax(model_output, 1)
        probs = probs.squeeze(0)

        topk = max(1, min(topk, len(labels)))
        top_probs, top_indexes = torch.topk(probs, topk)
        results = [(labels[i], float(c)) for c, i in zip(top_probs, top_indexes)]
        return results




    

