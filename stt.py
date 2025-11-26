import requests
from dotenv import load_dotenv
from os import environ

load_dotenv()

API_KEY = environ["MISTRAL_API_KEY"]  # replace with your key
AUDIO_FILE = "assets/sound.wav"          # your WAV file
MODEL = "voxtral-mini-latest"     # transcription model

url = "https://api.mistral.ai/v1/audio/transcriptions"

with open(AUDIO_FILE, "rb") as f:
    files = {"file": (AUDIO_FILE, f, "audio/wav")}
    data = {"model": MODEL, "language": "en"}

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(url, headers=headers, files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print("Transcription:", result.get("text", "No text returned"))
else:
    print("Error:", response.status_code, response.text)

