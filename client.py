# client.py
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

status = '0'
printed = '0'
co_sofa = '0'

# Numbers to send to the server
stst = '3'
ststt = '4'


def read():
    # Arduino reads this in a another thread for to optimize for speed.
    global status
    global ser

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            status = line


def updateCo(x):
    global co_sofa
    if co_sofa != x:
        co_sofa = x
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
        print(decoded)
        updateCo(decoded)


# Start reading serial from the arduino
arduinoRead = Thread(target=read)
arduinoRead.start()

while True:
    print(status)
    if status is '1':
        conne(stst)
    elif status is '0':
        conne(ststt)
    else:
        conne(ststt)

    sleep(.5)
