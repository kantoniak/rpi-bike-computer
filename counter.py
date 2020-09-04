import Adafruit_SSD1306
import RPi.GPIO as GPIO
import time
import signal
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

should_close = False

def handle_signals(signum, frame):
    global should_close
    should_close = True

signal.signal(signal.SIGINT, handle_signals)
signal.signal(signal.SIGTERM, handle_signals)

# Diode pins
BTN_PIN = 22 # Out from bike
LED_PIN = 17 # Red LED
LAP_PIN = 27 # Green LED

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BTN_PIN, GPIO.IN)
GPIO.setup(LAP_PIN, GPIO.OUT, initial=GPIO.LOW)

# Display
display = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
display.begin()
display.clear()
display.display()

# Drawing setup
image = Image.new('1', (display.width, display.height))
font = ImageFont.load_default()

was_closed = GPIO.input(BTN_PIN)
first_lap = True
last_lap = 0
lap_on = False
while not should_close:
    closed = GPIO.input(BTN_PIN)
    GPIO.output(LED_PIN, closed)

    if (was_closed and not closed):
        new_time = time.time()
        print('LAP: ' + str(new_time - last_lap)
        last_lap = new_time
        GPIO.output(LAP_PIN, GPIO.HIGH)
        lap_on = True

        draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
        draw.text((0, 0), "LAP: " + str(last_lap),  font=font, fill=255)
        draw.text((0, 8), "SPEED: 0",  font=font, fill=255)
        draw.text((0, 16), "DIST: 0",  font=font, fill=255)
        disp.image(image)
        disp.display()

    if lap_on:
        delta = time.time() - last_lap
        #print(str(delta))
        if delta > 0.1:
            GPIO.output(LAP_PIN, GPIO.LOW)
            lap_on = False

    was_closed = closed
