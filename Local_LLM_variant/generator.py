# app/generator.py
import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
TIMEOUT = 300  # maximum wait time in seconds

def dockerfile_from_ollama(code: str) -> str:
    """
    Generate a Dockerfile using local Ollama Mistral model.
    Handles multiple Ollama JSON response formats.
    """
    try:
        prompt = (
            f"Generate only a valid Dockerfile for the following code:\n\n{code}\n\n"
            "Do not include explanations or markdown fences."
        )

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()

        # Handle multiple response formats
        dockerfile = ""
        if "response" in data:
            dockerfile = data["response"]
        elif "results" in data and isinstance(data["results"], list):
            dockerfile = data["results"][0].get("output", "")
        dockerfile = (dockerfile or "").strip()

        # Remove any leftover markdown fences
        dockerfile = re.sub(r"```[a-zA-Z]*", "", dockerfile).replace("```", "").strip()

        if not dockerfile:
            return "# Error: Empty response from Ollama"
        return dockerfile

    except Exception as e:
        return f"# Error generating with Ollama: {str(e)}"


def generate_dockerfile(code: str) -> str:
    """
    Unified entry point: always uses AI.
    """
    return dockerfile_from_ollama(code)
