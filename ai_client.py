import base64
import os
from pathlib import Path
from typing import Final

import requests


OPENAI_API_KEY: Final[str] = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_URL: Final[str] = "https://api.openai.com/v1/chat/completions"
MODEL_NAME: Final[str] = "gpt-4.1-mini"


class OpenAIConfigError(RuntimeError):
    pass


def _ensure_api_key() -> str:
    if not OPENAI_API_KEY:
        raise OpenAIConfigError(
            "OPENAI_API_KEY is not set. Please set it in your environment."
        )
    return OPENAI_API_KEY


def ask_ai_with_image(image_path: Path, prompt: str) -> str:
    """
    Send an image + text prompt to OpenAI's gpt-4.1-mini vision model
    and return the model's text response.
    """
    api_key = _ensure_api_key()

    with image_path.open("rb") as f:
        b64_image = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64_image}",
                        },
                    },
                ],
            }
        ],
        "max_tokens": 150,
        "temperature": 0.3,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected OpenAI response format: {data}") from exc


