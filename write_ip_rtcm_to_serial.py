# Usage: 
# 1. You set the remoteServer and remoteServerPort variables below to an IP/PORT broadcasting RTCM messages
# 2. You set the connectedSerialDeviceName and connectedSerialDeviceBaudRate variables to the Name/Baud of your connected serial device
# 3. You run this command: python write_ip_rtcm_to_serial.py
# 
# This will read RTCM messages from the give IP/PORT and 
# write them to your connected serial device

import serial
import socket
import base64
import sys

###########################################
###The server broadcasting RTCM messages###
###########################################
#You will want to change this IP to 
#some RTCM source within ~50km of 
#you unless you are fortunate
#enough to live within 
#50km of Foley, 
#Alabama
remoteServer = "205.172.52.26"

##############################################
###The server's port emitting RTCM messages###
##############################################
#Again, you'll want to change this to 
#your RTCM provider's PORT
remoteServerPort = 19405

######################################################################################
###The name of the connected serial device that we will relay the RTCM messages to ###
######################################################################################
#If you don't know this, you can run the 
#list_attached_serial_devices.py script
#in this repo to get the name of 
#serial devices attached to
#the host machine
connectedSerialDeviceName = '/dev/tty.usbserial-DN009VQ0'

###################################################
###The baud rate of the connected serial device ###
###################################################
#You gotta get this baud rate right or
#it ain't gonna work bro
connectedSerialDeviceBaudRate = 115200

writeCount = 0;
RTCMv3_PREAMBLE = 0xD3
serialPort = serial.Serial(connectedSerialDeviceName, baudrate=connectedSerialDeviceBaudRate, timeout=0.2)
rtcmSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rtcmSocket.settimeout(0.5)
rtcmSocket.connect((remoteServer, remoteServerPort))
#serialPort.write(bytes("\r\n\r\n", "utf-8"))
#serialPort.write(bytes("interfacemode auto auto on\r\n\r\n", "utf-8"))
try:
        while True:
                try:
                        data = rtcmSocket.recv(1024)
                        if data[0] == RTCMv3_PREAMBLE:
                                serialPort.write(data)
                                writeCount += 1
                                print("wrote RTCM correction to serialPort {}".format(writeCount))
                                print("bytes: {}".format(data))
                                sys.stdout.flush()
                except:
                        nothing = 1
                if serialPort.inWaiting() > 10:
                        rcv = serialPort.read(serialPort.inWaiting())
                        print(rcv.decode("utf-8", "ignore"))
                        sys.stdout.flush()
finally:
        rtcmSocket.close()
        serialPort.close()

