import tkinter as tk
import threading
import time
from gpiozero import RGBLED, MotionSensor, DistanceSensor, Buzzer

# Define a global stop event for threads
stop_event = threading.Event()

def main(dt11=None, distanceSensor=None, ledRGB=None, debug=False):
    root = tk.Tk()
    global frequence
    frequence = 1
    printThread = None

    # dummy data
    if debug:
        class DummySensor:
            @property
            def temperature(self):
                return 22.5 
            @property
            def humidity(self):
                return 50
        class DummyDistance:
            @property
            def distance(self):
                return 0.5
        class DummyLED:
            red = green = blue = 0
            @property
            def color(self):
                return (self.red, self.green, self.blue)
        dt11 = DummySensor()
        distanceSensor = DummyDistance()
        ledRGB = DummyLED()
        print("DEBUG MODE ENABLED: Using dummy sensor values.")

    def ajouter_intervalle():
        global frequence
        print("+0.1 seconde d'intervalle")
        frequence += 0.1
        restart_print_thread()

    def diminuer_intervalle():
        global frequence
        print("-0.1 seconde d'intervalle")
        frequence -= 0.1
        restart_print_thread()

    def stop():
        print("Arrêt propre de la surveillance")
        stop_event.set()
        if printThread and printThread.is_alive():
            printThread.join()
        root.quit()

    def printInfo():
        while not stop_event.is_set():
            distanceInCentimeters = distanceSensor.distance * 100
            distanceInMeters = distanceSensor.distance
            if distanceInCentimeters < 10:
                ledRGB.red = 1
                ledRGB.blue = 0
                ledRGB.green = 0
            elif distanceInCentimeters >= 10 and distanceInCentimeters <= 30:
                ledRGB.red = 1
                ledRGB.blue = 0
                ledRGB.green = 1
            else:
                ledRGB.red = 0
                ledRGB.blue = 0
                ledRGB.green = 1
            print("Seconde ", frequence, " : Température : ", dt11.temperature, "C  Humidité ", dt11.humidity, "    Distance ", distanceInMeters, "m RGBLED ", ledRGB.color)
            time.sleep(frequence)

    def restart_print_thread():
        nonlocal printThread
        stop_event.set()
        if printThread and printThread.is_alive():
            printThread.join()
        stop_event.clear()
        printThread = threading.Thread(target=printInfo)
        printThread.start()

    # Buttons frame
    btn_frame = tk.Frame(root)
    btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

    button_border_forward = tk.Frame(btn_frame, highlightbackground="black", highlightthickness=4, bd=0)
    btn_forward = tk.Button(button_border_forward, text="+0.1 seconde d'intervalle", width=16, height=3, 
                            command=ajouter_intervalle, borderwidth=0, wraplength=75)
    btn_forward.pack()  # no padding inside frame
    button_border_forward.pack(side=tk.LEFT, padx=8)  # spacing between buttons

    button_border_left = tk.Frame(btn_frame, highlightbackground="black", highlightthickness=4, bd=0)
    btn_left = tk.Button(button_border_left, text="-0.1 seconde d'intervalle", width=16, height=3, 
                        command=diminuer_intervalle, borderwidth=0, wraplength=75)
    btn_left.pack()
    button_border_left.pack(side=tk.LEFT, padx=8)

    button_border_clear = tk.Frame(btn_frame, highlightbackground="black", highlightthickness=4, bd=0)
    btn_clear = tk.Button(button_border_clear, text="Arrêt propre de la surveillance", width=16, height=3, 
                        command=stop, borderwidth=0, wraplength=75)
    btn_clear.pack()
    button_border_clear.pack(side=tk.LEFT, padx=8)



    btn_forward.pack(side=tk.LEFT, padx=8, pady=6)
    btn_left.pack(side=tk.LEFT, padx=8, pady=6)
    btn_clear.pack(side=tk.LEFT, padx=8, pady=6)

    printThread = threading.Thread(target=printInfo)
    printThread.start()
    root.mainloop()

if __name__ == "__main__":
    main(debug=True)  # runs interface with dummy sensors
