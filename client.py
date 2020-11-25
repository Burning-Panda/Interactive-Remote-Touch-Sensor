# client.py
# Initial Imports
import socket
from time import sleep
import serial
from threading import Thread

# get server machine
HOST = '192.168.1.220'
# HOST = '10.53.90.241'
PORT = 5588

# Arduino USB
ard_usb = '/dev/ttyUSB0'

# Arduino Serial setup
ser = serial.Serial(ard_usb, 9600, timeout=.1)
ser.flush()

# Initial Global variables.
status = '0'
printed = '0'
co_sofa = '0'

# Numbers to send to the server
stst = '3'
ststt = '4'

# Read the arduino serial. Runs in a different thread to allow for faster and more accurate read speeds.
def read():
    global status
    global ser

    while True:
        # Check if arduino is plugged in, else ignore.
        if ser.in_waiting > 0:
             # Reads line and converts it to UTF-8
            line = ser.readline().decode('utf-8').rstrip()
            
            # Make sure that it reads the correct numbers. Anything above 1 should be ignored.
            if int(line) <= 2:
                status = line


def updateCo(x):
    global co_sofa
    
    # Checks if the variable is the same, to minimize the amount of blinking on the arduino.
    if co_sofa != x:
        co_sofa = x
        
        # Writes to the arduino and updates the light, if it should be on or off.
        encoded = co_sofa.encode()
        ser.write(encoded)


def conne(x):
    # How the raspberry talks to the other sofa

    global co_sofa
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connection to hostname on the port.
    s.connect((HOST, PORT))

    msg = str(x)
    s.send(msg.encode('ascii'))
    # Receive no more than 1024 bytes
    tm = s.recv(1024)

    s.close()
    decoded = tm.decode('ascii')

    if decoded != co_sofa:
        # print(decoded)
        updateCo(decoded)


# Start reading serial from the arduino
arduinoRead = Thread(target=read)
arduinoRead.start()

while True:
    # print(status)
    if status is '1':
        conne(stst)
    else:
        conne(ststt)

    sleep(.5)
