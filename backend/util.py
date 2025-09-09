import torch
import torch.nn.functional as F
from torchvision import transforms as T
from PIL import Image
import json
from io import BytesIO
from starlette.datastructures import UploadFile
import io
from PIL import UnidentifiedImageError
from PIL import ImageOps
from typing import Any, Dict, List, Union


allowed_ext = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

def file_lower(img_file): # "banana.jpg"
    img_file = img_file.split(".")
    ext = "." + img_file[-1].lower()
    return ext

def allow_img(file_name):
    name = file_lower(file_name)
    if name in allowed_ext:
        return True
    return False

    # This allows differnt kind of source into plan bytes
def read_bytes(src):
    if isinstance(src, bytes):
        return src
    elif isinstance(src, str):
        return open(src, "rb").read()
    elif isinstance(src, BytesIO):
        return src.getvalue()
    elif isinstance(src, UploadFile): 
        data = src.file.read()
        try:
            src.file.seek(0)
        except Exception:
            pass
        return data
    else:
        raise TypeError(f"Unsupported type: {type(src)}")


    # This takes the read_bytes and check if it's a valid image and return the photo after converting it to rgb
def open_img(file):
    raw_image = read_bytes(file)
    buffer = io.BytesIO(raw_image)
    try:
        image = Image.open(buffer)
    except UnidentifiedImageError:
        raise ValueError("Not a valid image")
    
    image = ImageOps.exif_transpose(image)
    return image.convert("RGB")

    # Clears and double check the size before display
def load_pil_for_display(src, max_side=1024):
    image = open_img(src)
    width, height = image.size
    longest = max(width, height)
    if longest > max_side:
        scale = max_side / longest
        new_width, new_height = (int(width * scale)),(int(height * scale))
        image = image.resize((new_width, new_height))
        return image
    return image

def get_inference_transform():
    return T.Compose([
        T.Resize(256),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225])
    ])
transform = get_inference_transform()

def load_tensor_for_model(img_file):
    image = open_img(img_file)
    tensor = transform(image)
    tensor = tensor.unsqueeze(0)
    return tensor

def get_device():
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"


def idx_to_label(labels: Union[List[str], Dict[str, Any]], idx: int) -> str:

    if isinstance(labels, list):
        return labels[idx]
    key = str(idx)
    if key not in labels:
        raise KeyError(f"Label index {idx} not found in mapping")
    return labels[key]










