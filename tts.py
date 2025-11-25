import subprocess

def speak(text):
    """
    Speak text using eSpeak NG with:
    - voice: en-us
    - pitch: 30
    - speed: 125
    """
    cmd = [
        "espeak-ng",
        "-v", "en-us",
        "-p", "30",
        "-s", "125",
        text
    ]

    subprocess.run(cmd, check=True)

