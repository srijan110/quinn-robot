from walk import walk_front
from mistral_api import MistralChat
from dotenv import load_dotenv
import os
from tts import speak

load_dotenv()

API=os.getenv("MISTRAL_API_KEY")

system_prompt="You are Quinn, helpful robot. Speak clearly and directly. Give answers and instructions without unnecessary fluff. Always stay polite, accurate, and confident. If you don’t know something, say so. Refer to yourself as Quinn."

chat = MistralChat(api_key=API, system_prompt=system_prompt)

speak(chat.send("Who are you?"))
