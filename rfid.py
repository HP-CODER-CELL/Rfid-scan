import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Hold an RFID tag near the reader...")
    while True:
        id, text = reader.read()
        print(f"Detected RFID tag! ID: {id}, Text: {text}")
        print("Remove tag and present another to detect movement.")
except KeyboardInterrupt:
    print("Stopping RFID reader...")
finally:
    GPIO.cleanup()
