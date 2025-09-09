from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .load import get_model, get_labels
from .util import allow_img, load_tensor_for_model, get_device, idx_to_label
import torch


app = FastAPI()

origins = [
    "http://localhost:3000", "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"ok": True, "routes": ["/ping", "/docs", "/classify"]}

@app.get("/ping")
def ping():
    return {"status": "ok", "service": "EcoVision API"}


@app.post("/predict")
async def predict(file: UploadFile):
    if not allow_img(file.filename):
        raise HTTPException(400, "Unsupported file type")

    model = get_model()
    labels = get_labels()

    tensor = load_tensor_for_model(file).to(get_device())

    model.eval()
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)
        idx = probs.argmax(dim=1).item()
        confidence = probs[0, idx].item()

    return {
        "index": idx,
        "label": idx_to_label(labels, idx),
        "confidence": confidence
    }
