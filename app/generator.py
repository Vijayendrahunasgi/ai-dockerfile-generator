# app/generator.py

import os
import re
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch credentials/config from environment
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  # ends with /
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "o4-mini")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
TIMEOUT = 300  # seconds

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=AZURE_API_VERSION
)

def dockerfile_from_azure(code: str) -> str:
        prompt = (
            f"Analyze the following code and generate only a valid Dockerfile that installs dependencies, "
            f"sets environment variables, exposes ports, and starts the app:\n\n"
            f"Respond ONLY with the Dockerfile.\n\n"
            f"{code}\n\n"
        )
        


        # Use chat completions API for more robust prompting
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[{
                "role": "system",
                "content": "You are an expert DevOps and Dockerfile generator. Always respond ONLY with a valid Dockerfile, never explanations or markdown formatting."
            }, {
                "role": "user",
                "content": prompt
            }],
            max_completion_tokens=2000,
            #temperature=0.25,
            timeout=TIMEOUT  # for OpenAI SDK >= 1.16.0
        )



        # Extract the Dockerfile result
        dockerfile = response.choices[0].message.content.strip()

        # Remove triple backticks and optional language specifier
        dockerfile = re.sub(r"`{3,}[\w]*", "", dockerfile)
        dockerfile = dockerfile.strip()

        if not dockerfile:
            return "# Error: Empty response from Azure OpenAI"
        return dockerfile

def generate_dockerfile(code: str) -> str:
    """
    Unified entry point: always uses Azure OpenAI.
    """
    return dockerfile_from_azure(code)
