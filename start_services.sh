#!/bin/bash

# Navigate to the directory
cd /home/Desktop/Toyon-Kitchenette-Unlock

# Activate the virtual environment
source venv/bin/activate

# Start ngrok
ngrok http --domain=humorous-frankly-skunk.ngrok-free.app 3000 &

# Execute the Python script
python unlock.py