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
        return src.file.read()
    else:
        raise TypeError("Unsupported type")
    

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

transform = T.Compose([
T.Resize(256),
T.CenterCrop(224),
T.ToTensor(),
T.Normalize(mean=[0.485, 0.456, 0.406],
std=[0.229, 0.224, 0.225]
    ) 
])

def load_tensor_for_model(img_file):
    image = open_img(img_file)
    tensor = transform(image)
    tensor = tensor.unsqueeze(0)
    return tensor










