from flask import Flask, request
#import dotenv
from flask import Flask, request
from gtts import gTTS 
import os
import RPi.GPIO as GPIO
from enum import Enum
import time


#dotenv.load_dotenv()

#STartup
#cd to directory
#source venv/bin/activate
#ngrok http --domain=humorous-frankly-skunk.ngrok-free.app 3000
#python unlock.py


app = Flask(__name__)

switch = 4
motor_enable = 22
motor_control = 27

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(switch, GPIO.IN)
GPIO.setup(motor_enable, GPIO.OUT)
GPIO.setup(motor_control, GPIO.OUT)
GPIO.output(motor_enable, 0)
GPIO.output(motor_control, 0)

class State(Enum):
    LOCKED = 0
    UNLOCKED = 1
    UNLOCKING = 2
    RELOCKING = 3
    ERROR = 4

def move_motor(dir, timeout, debounce_time=0.2):
    arm_start_time = time.time() #start time of arm movement

    #drive motors
    GPIO.output(motor_enable, dir)
    GPIO.output(motor_control, not dir)
    time.sleep(debounce_time)

    #wait for limit switch to trigger or timeout
    while GPIO.input(switch) == 0 and time.time() - arm_start_time < timeout:
        time.sleep(0.1)
    if time.time() - arm_start_time > timeout:
        print("Error: didn't reach limit switch in time")

    GPIO.output(motor_enable, 0)
    GPIO.output(motor_control, 0)


# time.sleep(2)

# print("moving")
# move_motor(0, 6, 1) #1: moving down
# move_motor(1, 6, 1) #1: moving up

# myobj = gTTS(text=f"Welcome, Lawton. Please clean up after yourself, and report any issues with the kitchenette to the google form.", lang="en", slow=False) 

# myobj.save("welcome.mp3") 
# os.system("mpg321 welcome.mp3")

@app.route('/webhook', methods=['POST'])
def webhook():

    data = request.json
    name = data[0]['answer']
    print(name)  # or process the data as needed

    myobj = gTTS(text=f"Welcome, {name}. Please clean up after yourself, and report any issues with the kitchenette to the google form.", lang="en", slow=False) 

    myobj.save("welcome.mp3") 
    os.system("mpg321 welcome.mp3")

    move_motor(0, 6, 1) #1: moving down
    time.sleep(2)
    move_motor(1, 6, 1) #1: moving up

    return "Webhook received", 200

if __name__ == '__main__':
    app.run(debug=True, port=3000)

