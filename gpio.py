import RPi.GPIO as GPIO
import time

# List of GPIO pins
GPIO_PINS = [13, 19, 26]

# Setup
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering

# Set up each pin as an output
for pin in GPIO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Ensure all pins are initially off

def main():
    try:
        print("Starting GPIO control script.")
        
        # Iterate through each pin in the list
        for pin in GPIO_PINS:
            print(f"Turning on LED connected to pin {pin}...")
            GPIO.output(pin, GPIO.HIGH)  # Turn on the LED
            time.sleep(5)  # Keep it on for 5 seconds
            GPIO.output(pin, GPIO.LOW)  # Turn off the LED
            print(f"Turning off LED connected to pin {pin}...")

    except KeyboardInterrupt:
        print("Script interrupted by user.")
        
    finally:
        # Cleanup
        print("Cleaning up GPIO...")
        GPIO.cleanup()

if __name__ == '__main__':
    main()
