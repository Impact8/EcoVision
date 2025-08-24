from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware


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

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    return {"ok": True, "label": "recycle", "confidence": 0.73}

