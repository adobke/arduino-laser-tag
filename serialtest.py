import time
import serial
import thread

def xConnect():
    ser = serial.Serial('/dev/ttyUSB0',57600,timeout=1)
    time.sleep(1)
    ser.write("<a>")
    if ser.inWaiting()>0:
        ser.flushInput()
        print 'connected!'
        return ser
    else:
        print 'no connection'
        return xConnect()

def write(ser,string):
    ser.write("<")
    for char in string:
        ser.write(string)
    ser.write(">")

def main():
    ser = xConnect()
    thread.start_new_thread(monitor,(ser,))
    while True:
        write(ser,raw_input(">> "))

def monitor(ser):
    while(True):
        if ser.inWaiting()>0:
            data = ser.readline()
            if not data=="\n":
                print "\t\t\t >>" + data[:-1]
