from flask import Flask, request, jsonify, render_template, send_file
import pathlib
from tts import speak
from dotenv import load_dotenv
from os import environ
from mistral_api import MistralChat

load_dotenv()

mistral = MistralChat(environ['MISTRAL_API_KEY'], "You are Quinn Robot. Give short to medium sized answers only")

app = Flask(__name__)

import subprocess

capture_image = ["rpicam-still", "-o", "static/image.png", "-t", "1", "--width", "800", "--height", "600"]

convert_wav = ["ffmpeg", "-y", "-i", "assets/rec.webm", "assets/rec.wav"]

# Shared state
state = {"direction": None}
messages = ''

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/control")
def control():
    return render_template("control.html")


# API for direction change
@app.post("/api/set-direction")
def set_direction():
    d = request.json.get("dir")
    state["direction"] = d
    return {"ok": True}


# API for live status
@app.get("/api/get-status")
def get_status():
    return {"direction": state["direction"]}


@app.route("/chat")
def chat():
    return render_template("chat.html")

# API for chat
@app.post("/api/chat-post")
def chat_post():
    text = request.json.get("text", "").strip()
    if text:
        messages = text
        speak(mistral.send(text))
    return {"ok": True}

@app.get("/api/chat-get")
def chat_get():
    return {"messages": messages}

@app.get("/view-image")
def view_image():
    return render_template("view_image.html")

@app.get("/output-image")
def output_image():
    subprocess.run(capture_image, check=True)
    return send_file("static/image.png", mimetype="image/jpeg")

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    file = request.files["file"]
    file.save('assets/rec.webm')
    
    subprocess.run(convert_wav, check=True)
 
    text = mistral.send_stt('assets/rec.wav')
    print(text)
    text = mistral.send_llm(text)
    speak(text)

    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

