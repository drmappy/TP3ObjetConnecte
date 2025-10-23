import tkinter as tk
import threading
import time

# Define a global stop event for threads
stop_event = threading.Event()

def main(dt11, distanceSensor, ledRGB):
    root = tk.Tk()
    global frequence
    frequence = 1
    printThread = None

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
        distanceInCentimeters = distanceSensor.distance * 100
        distanceInMeters = distanceSensor.distance
        while not stop_event.is_set():
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

    btn_forward = tk.Button(btn_frame, text="+0.1 seconde d'intervalle", width=16, height=3, command=ajouter_intervalle, borderwidth=10, wraplength=75)
    btn_left = tk.Button(btn_frame, text="-0.1 seconde d'intervalle", width=16, height=3, command=diminuer_intervalle, borderwidth=10, wraplength=75)
    btn_clear = tk.Button(btn_frame, text="Arrêt propre de la surveillance", width=16, height=3, command=stop, borderwidth=10, wraplength=75)

    btn_forward.pack(side=tk.LEFT, padx=8, pady=6)
    btn_left.pack(side=tk.LEFT, padx=8, pady=6)
    btn_clear.pack(side=tk.LEFT, padx=8, pady=6)

    printThread = threading.Thread(target=printInfo)
    printThread.start()
    root.mainloop()

if __name__ == "__main__":
    print("Not to be used in main.")