# server.py
import socket
from time import sleep
import serial
from threading import Thread


# get local machine name
host = "0.0.0.0"
port = 5588

status = '0'
printed = '0'
co_sofa = '0'

# Numbers to send to client
stst = '3'
ststt = '4'

# Setup serial.
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=.1)
ser.flush()


def read():
    global status
    global ser

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if int(line) < 2:
                status = line


def t():
    global printed
    global status
    while True:
        if status != printed:
            print(f"Switched from: {printed}, To: {status}")
            printed = status


def updateCo(x):
    global co_sofa
    if co_sofa != x:
        co_sofa = x
        # print('Switched')
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

arduinoRead = Thread(target=read)
arduinoRead.start()

# varicheck = Thread(target=t)
# varicheck.start()


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
    elif status is '0':
        clientsocket.send(ststt.encode('ascii'))
    else:
        clientsocket.send(ststt.encode('ascii'))
    clientsocket.close()
    print(co_sofa)
