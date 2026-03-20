from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from pydantic import BaseModel
from vision_test import run_vision_analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "fe" / "uploads"

class AnalyzeRequest(BaseModel):
    filename: str
    prompt: str = "What are the items that can be picked up by the robot?"

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    image_path = UPLOAD_DIR / request.filename
    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {image_path}")
    try:
        response_text = run_vision_analysis(image_path, request.prompt)
        return {"success": True, "response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Vision analysis API running"}
