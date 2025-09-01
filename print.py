import RPi.GPIO as GPIO
import time
import queue
import datetime
import subprocess

# BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Pin setup
BUTTON1_PIN = 20  # First button → previous date
BUTTON2_PIN = 21  # Second button → today's date

GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Queue for button press events (stores callables)
button_queue = queue.Queue()

# Actions
def print_prev_date():
    prev_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%y")
    print(prev_date)
    print_label(prev_date)

def print_today_date():
    today = datetime.date.today().strftime("%m/%d/%y")
    print(today)
    print_label(today)

def print_label(text):
    fname="label.png"
    printer="DYMO LabelWriter 450 Turbo"
    media="media=oe_square-multipurpose-label_1x1in"
    
    subprocess.run(["convert", "-size", "150x150", "xc:white", "-pointsize", "60", "-fill", "black", "-gravity", "Center", "-annotate", "0", text, fname])
    subprocess.run(["lprint", "submit", "-d", printer, "-o", media, fname ])

# Callback for button 1
def button1_callback(channel):
    if GPIO.input(BUTTON1_PIN) == GPIO.HIGH:
        button_queue.put(print_prev_date)

# Callback for button 2
def button2_callback(channel):
    if GPIO.input(BUTTON2_PIN) == GPIO.HIGH:
        button_queue.put(print_today_date)

# Event detection
GPIO.add_event_detect(BUTTON1_PIN, GPIO.RISING, callback=button1_callback, bouncetime=50)
GPIO.add_event_detect(BUTTON2_PIN, GPIO.RISING, callback=button2_callback, bouncetime=50)

print("Press button 1 for previous date, button 2 for today's date (CTRL+C to exit)")

try:
    while True:
        try:
            action = button_queue.get(timeout=1)  # Get function
            action()  # Call function
        except queue.Empty:
            pass
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()
