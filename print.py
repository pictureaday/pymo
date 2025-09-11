import RPi.GPIO as GPIO
import os
import time
import queue
import datetime
import subprocess

# BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Pin setup

BUTTON1_PIN = 20
BUTTON2_PIN = 1
BUTTON3_PIN = 16
BUTTON4_PIN = 12
BUTTON5_PIN = 21
BUTTON6_PIN = 8
BUTTON7_PIN = 7
BUTTON8_PIN = 25

GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(BUTTON5_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON6_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON7_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON8_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Queue for button press events (stores callables)
button_queue = queue.Queue()

# Actions
def print_prev_date():
    prev_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%y")
    print(prev_date)
    print_label(prev_date)

def print_today_date_schoolmilk():
    today = datetime.date.today().strftime("%m/%d/%y")
    print(today)
    print_label("School\nMilk\n" + today)

def print_today_date_breastmilk():
    today = datetime.date.today().strftime("%m/%d/%y")
    print(today)
    print_label("Breastmilk\n" + today)

def print_today_date():
    today = datetime.date.today().strftime("%m/%d/%y")
    print(today)
    print_label(today)

# Plain names
def print_name_adult1():
    print_file_contents("adult1.txt", "24");
def print_name_adult2():
    print_file_contents("adult2.txt", "24");
def print_name_kid1():
    print_file_contents("kid1.txt");
def print_name_kid1():
    print_file_contents("kid1.txt");

def print_file_contents(fname, fontsize="30"):
    if os.path.isfile(fname) and os.access(fname, os.R_OK):
        file_object = open(fname)
        print_label(file_object.read(), fontsize)
    else:
        with open(fname, 'w') as file:
            file.write("Sample\nName")
        print(fname + " does not exist. Creating it now.")

        

def print_label(text, fontsize="30"):
    fname="label.png"
    print("fontsize: " + fontsize) 
    subprocess.run(["convert", "-size", "150x150", "xc:white", "-pointsize", fontsize, "-fill", "black", "-gravity", "Center", "-annotate", "0", text, fname])
    subprocess.run(["lp", "-o page-bottom=4", "-o page-top=4", "-o media=Custom.1x1in", fname ])

# Callback for button 1
def button1_callback(channel):
    if GPIO.input(BUTTON1_PIN) == GPIO.HIGH:
        button_queue.put(print_prev_date)
# Callback for button 2
def button2_callback(channel):
    if GPIO.input(BUTTON2_PIN) == GPIO.HIGH:
        button_queue.put(print_today_date_schoolmilk)
# Callback for button 3

def button3_callback(channel):
    if GPIO.input(BUTTON3_PIN) == GPIO.HIGH:
        button_queue.put(print_name_adult1)

# Callback for button 4
def button4_callback(channel):
    if GPIO.input(BUTTON4_PIN) == GPIO.HIGH:
        button_queue.put(print_name_kid1)

# Callback for button 5
def button5_callback(channel):
    if GPIO.input(BUTTON5_PIN) == GPIO.HIGH:
        button_queue.put(print_today_date)

# Callback for button 6
def button6_callback(channel):
    if GPIO.input(BUTTON6_PIN) == GPIO.HIGH:
        button_queue.put(print_today_date_breastmilk)

# Callback for button 7
def button7_callback(channel):
    if GPIO.input(BUTTON7_PIN) == GPIO.HIGH:
        button_queue.put(print_name_adult2)

# Callback for button 8
def button8_callback(channel):
    if GPIO.input(BUTTON8_PIN) == GPIO.HIGH:
        button_queue.put(print_name_kid2)


# Event detection
GPIO.add_event_detect(BUTTON1_PIN, GPIO.RISING, callback=button1_callback, bouncetime=50)
GPIO.add_event_detect(BUTTON2_PIN, GPIO.RISING, callback=button2_callback, bouncetime=50)
GPIO.add_event_detect(BUTTON3_PIN, GPIO.RISING, callback=button3_callback, bouncetime=50)
GPIO.add_event_detect(BUTTON4_PIN, GPIO.RISING, callback=button4_callback, bouncetime=50)
GPIO.add_event_detect(BUTTON5_PIN, GPIO.RISING, callback=button5_callback, bouncetime=50)
GPIO.add_event_detect(BUTTON6_PIN, GPIO.RISING, callback=button6_callback, bouncetime=50)
GPIO.add_event_detect(BUTTON7_PIN, GPIO.RISING, callback=button7_callback, bouncetime=50)
GPIO.add_event_detect(BUTTON8_PIN, GPIO.RISING, callback=button8_callback, bouncetime=50)

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

