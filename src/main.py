import time
import sys

try:
    from sensors import initialize_sensors, cleanup_sensors
    from gui import create_and_run_gui
    from config import BUZZER_DURATION, PIN_BUZZER
    from gpiozero import Buzzer
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("\nMake sure you're in the correct directory with:")
    print("  - config.py")
    print("  - sensors.py") 
    print("  - gui.py")
    sys.exit(1)


def wait_for_motion(motion_sensor):
    print("Faites un mouvement pour démarrer le programme...")
    motion_sensor.wait_for_motion()
    print("Merci, c'est parti!")


def signal_start(buzzer):
    buzzer.on()
    time.sleep(BUZZER_DURATION)
    buzzer.off()


def main(debug=False):
    sensors = None
    try:
        sensors = initialize_sensors(debug=debug)

        if sensors.get('dht11') is None:
            print("Warning: DHT11 sensor failed to initialize.")

        if not debug:
            wait_for_motion(sensors['motion_sensor'])

            signal_start(sensors['buzzer'])

            sensors['motion_sensor'].when_activated = None
            sensors['motion_sensor'].when_deactivated = None
        else:
            print("Merci, c'est parti! (mode debug)")

        create_and_run_gui(sensors)

    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur")
    except Exception as e:
        print("exception is in main")
        print(f"Erreur: {e}")
    finally:
        if sensors:
            cleanup_sensors(sensors)
        print("Programme terminé proprement")


if __name__ == "__main__":
 
    main(debug=False)