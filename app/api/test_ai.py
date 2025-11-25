from fastapi import APIRouter
import os
import requests

router = APIRouter()

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_ENDPOINT = os.getenv("RUNPOD_ENDPOINT")

@router.get("/test-ai")
def test_ai():
    url = os.getenv("RUNPOD_ENDPOINT")
    api_key = os.getenv("RUNPOD_API_KEY")

    payload = {
        "input": {
            "video_url": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"
        }
    }

    headers = {"Authorization": f"Bearer {api_key}"}

    r = requests.post(url, json=payload, headers=headers)
    return r.json()
