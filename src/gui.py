import tkinter as tk
import threading
import time
import sys
from config import (
    DEFAULT_FREQUENCY, FREQUENCY_STEP,
    DISTANCE_RED_THRESHOLD, DISTANCE_YELLOW_MAX,
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_PADDING,
    BUTTON_BORDER_WIDTH, BUTTON_WRAP_LENGTH
)


class SensorMonitorGUI:
    
    def __init__(self, sensors):
        self.sensors = sensors
        self.frequency = DEFAULT_FREQUENCY
        self.stop_event = threading.Event()
        self.monitor_thread = None
        
        self.root = tk.Tk()
        self.root.title("Surveillance des capteurs")
        self._create_widgets()
        self._start_monitoring()
    
    def _create_widgets(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self._create_button(
            btn_frame,
            text="+0.1 seconde d'intervalle",
            command=self._increase_frequency
        )
        
        self._create_button(
            btn_frame,
            text="-0.1 seconde d'intervalle",
            command=self._decrease_frequency
        )
        
        self._create_button(
            btn_frame,
            text="Arrêt propre de la surveillance",
            command=self._stop_monitoring
        )
    
    def _create_button(self, parent, text, command):
        border_frame = tk.Frame(
            parent,
            highlightbackground="black",
            highlightthickness=BUTTON_BORDER_WIDTH,
            bd=0
        )
        
        button = tk.Button(
            border_frame,
            text=text,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=command,
            borderwidth=0,
            wraplength=BUTTON_WRAP_LENGTH
        )
        button.pack()
        border_frame.pack(side=tk.LEFT, padx=BUTTON_PADDING)
    
    def _increase_frequency(self):
        self.frequency += FREQUENCY_STEP
        print(f"+{FREQUENCY_STEP} seconde d'intervalle")
        sys.stdout.flush()
        self._restart_monitoring()
    
    def _decrease_frequency(self):
        self.frequency = max(FREQUENCY_STEP, self.frequency - FREQUENCY_STEP)
        print(f"-{FREQUENCY_STEP} seconde d'intervalle")
        sys.stdout.flush()
        self._restart_monitoring()
    
    def _stop_monitoring(self):
        print("Arrêt propre de la surveillance")
        sys.stdout.flush()
        self.stop_event.set()
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        
        self.root.quit()
        self.root.destroy()
    
    def _monitor_sensors(self):
        print("Démarrage du fil de surveillance des capteurs...")  # Debugging thread start
        print(f"État initial de stop_event: {self.stop_event.is_set()}")  # Check initial state of stop_event
        sys.stdout.flush()
        iteration = 0

        while not self.stop_event.is_set():
            print("Entrée dans la boucle while de surveillance des capteurs.")  # Confirm entering the loop
            sys.stdout.flush()
            try:
                iteration += 1
                print(f" itération de surveillance {iteration}...")  # Debugging iteration
                sys.stdout.flush()

                distance_m = self.sensors['distance_sensor'].distance
                distance_cm = distance_m * 100
                temperature = self.sensors['dht11'].temperature
                humidity = self.sensors['dht11'].humidity

                self._update_led_color(distance_cm)

                print(
                    f"Seconde {iteration * self.frequency:.1f}: "
                    f"Température: {temperature}°C  "
                    f"Humidité: {humidity}%  "
                    f"Distance: {distance_m:.2f}m  "
                    f"RGBLED: {self._get_led_color_name()}"
                )
                sys.stdout.flush()

                time.sleep(self.frequency)

            except RuntimeError as e:
                # DHT11 can occasionally fail to read
                print(f"Erreur de lecture: {e}")
                sys.stdout.flush()
                continue
            except Exception as e:
                print(f"Erreur inattendue dans le thread: {e}")  # Debugging unexpected errors
                sys.stdout.flush()
                break

        print("Le fil de surveillance des capteurs s'est arrêté.")  # Debugging thread stop
        sys.stdout.flush()
    
    def _update_led_color(self, distance_cm):
        led = self.sensors['led_rgb']
        
        if distance_cm < DISTANCE_RED_THRESHOLD:
            led.red = 1
            led.green = 0
            led.blue = 0
        elif distance_cm <= DISTANCE_YELLOW_MAX:
            led.red = 1
            led.green = 1
            led.blue = 0
        else:
            led.red = 0
            led.green = 1
            led.blue = 0
    
    def _get_led_color_name(self):
        color = self.sensors['led_rgb'].color
        
        if color == (1, 0, 0):
            return "rouge"
        elif color == (1, 1, 0):
            return "jaune"
        elif color == (0, 1, 0):
            return "verte"
        else:
            return str(color)
    
    def _start_monitoring(self):
        print("Starting the monitoring thread...")  # Debugging thread start
        sys.stdout.flush()
        self.monitor_thread = threading.Thread(
            target=self._monitor_sensors,
            daemon=True
        )
        self.monitor_thread.start()
    
    def _restart_monitoring(self):
        self.stop_event.set()
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        
        self.stop_event.clear()
        self._start_monitoring()
    
    def run(self):
        self.root.mainloop()


def create_and_run_gui(sensors):
    gui = SensorMonitorGUI(sensors)
    gui.run()