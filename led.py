import RPi.GPIO as GPIO

red = 14
green = 15
buzzer = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

def setup():
    GPIO.output(red, True)
    GPIO.output(green, False)
def running():
    GPIO.output(red, False)
    GPIO.output(green, True)
def detected():
    GPIO.output(red, True)
    GPIO.output(green, True)
if __name__ == "__main__":
    pass
