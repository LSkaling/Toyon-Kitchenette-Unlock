from flask import Flask, request
import dotenv
from flask import Flask, request
from gtts import gTTS 
import os
import RPi.GPIO as GPIO
from enum import Enum
import time


dotenv.load_dotenv()


app = Flask(__name__)

switch = 26
motor_a = 19
motor_b = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(switch, GPIO.IN)
GPIO.setup(motor_a, GPIO.OUT)
GPIO.setup(motor_b, GPIO.OUT)

class State(Enum):
    LOCKED = 0
    UNLOCKED = 1
    UNLOCKING = 2
    RELOCKING = 3
    ERROR = 4

def move_motor(dir, timeout, debounce_time=0.5):
    arm_start_time = time.time() #start time of arm movement

    #drive motors
    GPIO.output(motor_a, dir)
    GPIO.output(motor_b, not dir)
    time.sleep(debounce_time)

    #wait for limit switch to trigger or timeout
    while GPIO.input(switch) == 0 and time.time() - arm_start_time < timeout:
        time.sleep(0.1)
    if time.time() - arm_start_time < timeout:
        print("Error: didn't reach limit switch in time")
        return State.ERROR
    
    #TODO: log amount of time it took

@app.route('/webhook', methods=['POST'])
def webhook():

    data = request.json
    name = data[0]['answer']
    print(name)  # or process the data as needed

    # myobj = gTTS(text=f"Welcome, {name}. Please clean up after yourself, and report any issues with the kitchenette to the google form. Happy sheffin!", lang="en", slow=False) 

    # myobj.save("welcome.mp3") 
    # os.system("mpg321 welcome.mp3")

    move_motor(1, 10)
    time.sleep(2)
    move_motor(0, 10)

    return "Webhook received", 200

if __name__ == '__main__':
    app.run(debug=True, port=3000)

