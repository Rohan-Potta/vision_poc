import requests
import base64
from pathlib import Path

# --------------------------------------------------
# DEFAULT IMAGE PATH (used only if no path is provided)
# --------------------------------------------------
IMAGE_PATH = Path(r"C:\Users\rohan\Coding\vision models\fe\uploads\Screenshot 2026-03-19 163104.png")

# --------------------------------------------------
# SYSTEM PROMPT (MODEL BEHAVIOR)
# --------------------------------------------------
SYSTEM_PROMPT = """
You are a robot perception system.

Rules:
- Focus only on objects visible in the image.
- Assume objects can be picked up.
- Be concise and practical.
- Prefer actionable answers.
"""


def encode_image(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analysis_prompt(user_request: str) -> str:
    return f"""
{SYSTEM_PROMPT}

Analyze the provided image carefully.

User request:
{user_request}

Respond clearly.
"""


def run_vision_analysis(image_path: Path, user_request: str = "What are the items that can be picked up by the robot?") -> str:
    """Returns the model response text."""
    if not image_path.exists():
        raise FileNotFoundError("Image path does not exist: {image_path}")

    image_data = encode_image(image_path)
    final_prompt = analysis_prompt(user_request)

    payload = {
        "model": "moondream",
        "prompt": final_prompt,
        "images": [image_data],
        "stream": False,
        "options": {"temperature": 0.2},
    }

    response = requests.post("http://localhost:11434/api/generate", json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Ollama request failed: {response.status_code} {response.text}")

    result = response.json()
    return result.get("response", "No response returned")


if __name__ == "__main__":
    print("Running local test for vision analysis")
    result = run_vision_analysis(IMAGE_PATH)
    print("Model response:\n", result)
