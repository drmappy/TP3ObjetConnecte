HARDWARE_AVAILABLE = False
IMPORT_ERROR_MSG = None

try:
    from config import (
        PIN_LED_RED, PIN_LED_GREEN, PIN_LED_BLUE,
        PIN_MOTION, PIN_DISTANCE_ECHO, PIN_DISTANCE_TRIGGER,
        PIN_DHT11 #PIN_BUZZER
    )
    import psutil
    import board
    print(dir(board))
    from gpiozero import RGBLED, MotionSensor, DistanceSensor #Buzzer
    from adafruit_dht import DHT11
    HARDWARE_AVAILABLE = True
except (ImportError, NotImplementedError) as e:
    IMPORT_ERROR_MSG = str(e)
    PIN_LED_RED = PIN_LED_GREEN = PIN_LED_BLUE = 0
    PIN_MOTION = PIN_DISTANCE_ECHO = PIN_DISTANCE_TRIGGER = 0
    PIN_DHT11 = 0#PIN_BUZZER 


def clean_gpio_processes():
    if not HARDWARE_AVAILABLE:
        return
    
    try:
        for proc in psutil.process_iter():
            if proc.name() in ['libgpiod_pulsein', 'libgpiod_pulsei']:
                proc.kill()
    except Exception as e:
        print(f"Warning: Could not clean GPIO processes: {e}")


def initialize_sensors(debug=False):
    if debug or not HARDWARE_AVAILABLE:
        if not HARDWARE_AVAILABLE and not debug:
            print("=" * 60)
            print("Hardware libraries not available - using debug mode")
            print("Reason:", IMPORT_ERROR_MSG[:100] if IMPORT_ERROR_MSG else "Unknown")
            print("=" * 60)
        return _create_dummy_sensors()
    
    clean_gpio_processes()
    
    led_rgb = RGBLED(
        red=PIN_LED_RED,
        green=PIN_LED_GREEN,
        blue=PIN_LED_BLUE,
        active_high=False
    )
    
    motion_sensor = MotionSensor(PIN_MOTION)
    distance_sensor = DistanceSensor(
        echo=PIN_DISTANCE_ECHO,
        trigger=PIN_DISTANCE_TRIGGER
    )
    dht11_sensor = DHT11(getattr(board, f'D{PIN_DHT11}'))  # Updated to use GPIO pin
    # buzzer = Buzzer(PIN_BUZZER)
    
    return {
        'led_rgb': led_rgb,
        'motion_sensor': motion_sensor,
        'distance_sensor': distance_sensor,
        'dht11': dht11_sensor,
        # 'buzzer': buzzer
    }


def _create_dummy_sensors():
    class DummyDHT11:
        @property
        def temperature(self):
            return 22.5
        
        @property
        def humidity(self):
            return 50
        
        def exit(self):
            pass
    
    class DummyDistance:
        @property
        def distance(self):
            import random
            return round(random.uniform(0.05, 1.0), 2)
    
    class DummyLED:
        def __init__(self):
            self.red = 0
            self.green = 0
            self.blue = 0
        
        @property
        def color(self):
            return (self.red, self.green, self.blue)
        
        def close(self):
            pass
    
    class DummyMotionSensor:
        def __init__(self):
            self.when_activated = None
            self.when_deactivated = None
        
        def wait_for_motion(self):
            print("(Dummy motion sensor - motion detected immediately)")
        
        def close(self):
            pass
    
    # class DummyBuzzer:
    #     def on(self):
    #         print("(Buzzer: BEEP)")
        
    #     def off(self):
    #         print("(Buzzer: OFF)")
        
    #     def close(self):
    #         pass
    
    print("DEBUG MODE: Using dummy sensor values.")
    
    return {
        'led_rgb': DummyLED(),
        'motion_sensor': DummyMotionSensor(),
        'distance_sensor': DummyDistance(),
        'dht11': DummyDHT11(),
        # 'buzzer': DummyBuzzer()
    }


def cleanup_sensors(sensors):
    if not sensors:
        return
    
    try:
        dht = sensors.get('dht11')
        if dht and hasattr(dht, 'exit'):
            dht.exit()
        
        for key in ['led_rgb', 'motion_sensor', 'distance_sensor']:
            component = sensors.get(key)
            if component and hasattr(component, 'close'):
                component.close()
    except Exception as e:
        print(f"Error during cleanup: {e}")