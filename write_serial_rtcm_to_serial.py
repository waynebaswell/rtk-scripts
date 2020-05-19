#read rtcm and write to serial
import serial
import socket
import base64
import sys
import time

print("here we go 1 ...")
writeCount = 0;
#RTCMv3_PREAMBLE = 0xD3

#writeSerialPort = serial.Serial('/dev/tty.usbserial-DN009VQ0', baudrate=115200, timeout=0.1) #COM13

writeSerialPort = serial.Serial('/dev/tty.usbserial-DN009VQ0', baudrate=115200, timeout=0.2)
readSerialPort = serial.Serial('/dev/tty.usbmodem14131', baudrate=115200, timeout=0.2)
#readSerialPort = serial.Serial('/dev/tty.usbserial-FT9L299I', baudrate=57600, timeout=0.1)
print("here we go 1.1 ...")
try:
        while True:
                try:
                        #data = rtcmSocket.recv(1024)
                        #print("here we go 2...")
                        bytesToRead = readSerialPort.in_waiting
                        
                        if(bytesToRead > 0):
                                data = readSerialPort.read(bytesToRead)
                                print("bytes read: {}".format(bytesToRead))
                                print("bytes: {}".format(data))
                                #if data[0] != 0x1E:
                                writeSerialPort.write(data)
                                writeCount += 1
                                print("wrote RTCM correction to writeSerialPort {}".format(writeCount))
                except:
                        nothing = 1
                        print("Unexpected error:", sys.exc_info()[0])
                        
                sys.stdout.flush()
                
                if writeSerialPort.in_waiting > 10:
                        rcv = writeSerialPort.read(writeSerialPort.in_waiting)
                        print(rcv.decode("utf-8", "ignore"))
                        sys.stdout.flush()
                time.sleep(1)
finally:
        #rtcmSocket.close()
        writeSerialPort.close()
        readSerialPort.close()

