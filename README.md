# Vision POC

A small vision-language proof-of-concept combining:

- Frontend file upload + preview (`fe/server.js`, `fe/public/*`)
- FastAPI backend for image analysis (`be/app.py`)
- Local model call to Ollama API from `be/vision_test.py`

## Requirements

- Python 3.10+ (or 3.11+)
- Node.js 16+ (for frontend upload server)
- Ollama running locally with `moondream` model (or replace model name in `be/vision_test.py`)

## Setup

1. Clone repository and open terminal in project root.
2. Install backend dependencies from requirements:

```bash
cd be
pip install -r requirements.txt
```

3. Install frontend dependencies:

```bash
cd ../fe
npm install express multer
```

## Run

### 1) Start Ollama (must be running first)

Make sure Ollama is running and available at `http://localhost:11434/api/generate` with model `moondream`.

### 2) Start FastAPI backend

```bash
cd ../be
.venv\Scripts\activate            # Windows
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 3) Start frontend upload server

```bash
cd ../fe
npm start
```

Open `http://localhost:3000`.

## How to use

1. In browser, choose an image file.
2. Click `Upload`.
3. The frontend uploads to `fe/uploads`, then calls `http://localhost:8000/analyze`.
4. FastAPI reads the file, encodes base64, sends to Ollama, and returns the model response.
5. The UI shows the model response.

## Notes

- The analyze prompt is currently hardcoded to:
  `What are the items that can be picked up by the robot?`
- To change model prompt or model name, edit `be/vision_test.py`.
- If you use a different Ollama endpoint, update `be/vision_test.py` accordingly.

## Quick sanity check

- Backend health: `curl http://localhost:8000/`
- Frontend static site: `curl http://localhost:3000/`

Enjoy testing your vision-language POC!
