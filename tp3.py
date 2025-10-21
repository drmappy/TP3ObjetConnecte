from gpiozero import MotionSensor
from gpiozero import RGBLED
from gpiozero import DistanceSensor
import adafruit_dht
import turtle
import tkinter
from time import sleep

ledRGB = RGBLED(13, 19, 26)
motionSensor = MotionSensor(17)
distanceSensor = DistanceSensor(echo=16, trigger=12)
dt11 = adafruit_dht.DHT11(21)

def graphique():
    print()
def printInfo(frequence = 1):
    while True:
        print("Seconde ", frequence, " : Température ")
def mainCode():
    print("Inside main code")
    # Disable motion sensor 
    motionSensor.when_activated = None
    motionSensor.when_deactivated = None


motionSensor.when_activated = mainCode