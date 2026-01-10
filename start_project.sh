#!/bin/bash
source /home/srijan/project/venv/bin/activate

python /home/srijan/project/server.py & ngrok http 5000
