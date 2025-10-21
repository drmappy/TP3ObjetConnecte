from gpiozero import MotionSensor
from gpiozero import RGBLED
from gpiozero import DistanceSensor
import adafruit_dht
import turtle
import tkinter
import threading
from time import sleep
from interface import main

ledRGB = RGBLED(13, 19, 26)
motionSensor = MotionSensor(17)
distanceSensor = DistanceSensor(echo=16, trigger=12)
dt11 = adafruit_dht.DHT11(21)
frequence = 1

def mainCode():
    print("Merci, c'est parti!")
    # Disable motion sensor 
    motionSensor.when_activated = None
    motionSensor.when_deactivated = None
    main(dt11=dt11, distanceSensor=distanceSensor, ledRGB=ledRGB)


motionSensor.when_activated = mainCode