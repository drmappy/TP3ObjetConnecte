from gpiozero import MotionSensor, RGBLED, DistanceSensor, Buzzer
from adafruit_dht import DHT11
from interface import main
import board

ledRGB = RGBLED(13, 19, 26)
motionSensor = MotionSensor(17)
distanceSensor = DistanceSensor(echo=16, trigger=12)
dt11 = DHT11(board.D21)
buzzer = Buzzer(27)

def mainCode():
    ledRGB.active_high = False
    print("Merci, c'est parti!")
    buzzer.on()
    # Should add a delay?
    buzzer.off()
    motionSensor.when_activated = None
    motionSensor.when_deactivated = None
    main(dt11=dt11, distanceSensor=distanceSensor, ledRGB=ledRGB)


motionSensor.when_activated = mainCode