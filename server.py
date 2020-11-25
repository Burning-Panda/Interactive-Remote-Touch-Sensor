# server.py
# Initial imports.
import socket
from time import sleep
import serial
from threading import Thread


# get local machine name
host = "0.0.0.0"
port = 5588

# The usb port the arduino is plugged into
ard_usb = '/dev/ttyUSB0'

# Initial Global variables.
status = '0'
printed = '0'
co_sofa = '0'

# Numbers to send to client
stst = '3'
ststt = '4'

# Setup serial.
ser = serial.Serial(ard_usb, 9600, timeout=.1)
ser.flush()

# Read the arduino serial. Runs in a different thread to allow for faster and more accurate read speeds.
def read():
    global status
    global ser

    while True:
        # Check if arduino is plugged in, else ignore.
        if ser.in_waiting > 0:
            # Reads line and converts it to UTF-8
            line = ser.readline().decode('utf-8').rstrip()
            
            # Make sure that it reads the correct numbers. Anything above 2 should be ignored.
            if int(line) <= 2:
                status = line


def updateCo(x):
    global co_sofa
    
    # Checks if the variable is the same, to minimize the amount of blinking on the arduino.
    if co_sofa != x:
        co_sofa = x
        # print('Switched')
        
        # Writes to the arduino and updates the light, if it should be on or off.
        encoded = co_sofa.encode()
        ser.write(encoded)
    else:
        pass


# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

# Starts the arduino thread.
arduinoRead = Thread(target=read)
arduinoRead.start()


while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()

    # print("Got a connection from %s" % str(addr))

    getUpt = clientsocket.recv(1024).decode('ascii')
    if getUpt is not False or None:
        updateCo(getUpt)

    # clientsocket.send(status.encode('ascii'))
    if status is '1':
        clientsocket.send(stst.encode('ascii'))
    else:
        clientsocket.send(ststt.encode('ascii'))
    
    # Closes the connection to allow other sockets to be established.
    clientsocket.close()
    # print(co_sofa)
