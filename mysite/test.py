import serial
import time

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv

port = serial.Serial("/dev/ttyUSB2", baudrate=115200, timeout=1.2)

while True:
    print readlineCR(port)