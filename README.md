# EcoVision
FastAPI + React demo to classify an image as recycle/landfill (plastic, paper, metal, glass, cardboard, and trash).

Quick Start
-cd EcoVision
-python -m venv venv        # macOS/Linux
-source venv/bin/activate   # Windows
-pip install -r requirements.txt

Create backend/.env
-MODEL_PATH=backend/models/your_model.pt
-LABELS_PATH=backend/models/classes.json
-DEVICE=auto   # or cuda | mps | cpu

Run(from project root)
-uvicorn backend.app:app --reload

Frontend
-npm install

Create frontend/.env.local
-REACT_APP_API_URL=http://127.0.0.1:8000

Run
-npm start

Open the React app and you will see "Choose an image". Click that and upload a image and it will make a prediction.





