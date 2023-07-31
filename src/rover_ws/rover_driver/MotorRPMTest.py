# For windows go to device manager and look at COM devices, typically the only one listed is the USB to RS-232 cable, assume it's baud rate is 9600
# In terminal write "dmesg | grep FTDI" to detect Serial Converter Cable and assign it to device port (will most likely be ttyUSB0)
# To check port and baud rate, type "python -m serial.tools.miniterm" in Pi's command terminal


import serial                                   # Import PySerial (First time running code on new pi or windows machine run "pip install pyserial" in terminal to install)
import time                                     # Import Time
import re                                       # Import ReGex (First time running code on new pi or windows machine run "pip install regex" in terminal to install)

ser = serial.Serial('/dev/cu.usbserial-FT5P779S',9600)                # Establish COM port and baud rate to send commands thru (for linux or Raspberry Pi use '/dev/ttyUSBX')

ENC = 4000                                      # Encoder count for Nema 23 and Nema 17 motors
SMPL = 8000                                     # Default motor sampling rate

VTpos = 'VT=X \r'                               # Expression for positive VT values
VTneg = 'VT=-X \r'                              # Expression for negative VT values
Tval  = 'VT=X \r'

ser.write(b'Ba ')                             # Read Heat Flag (Bh)
time.sleep(1)
print(ser.read())

VTneg = VTneg.encode()                          # Encodes VTneg string into bytes for use with ser.write command
#ser.write(b'Z \r')
ser.write(b'ZS \r')                             # Clears motor flags (flags prevent further commands from being used)
ser.write(b'EIGN(2)')                           # Clears left hardware limit
ser.write(b'EIGN(3)')                           # Clears right hardware limit
ser.write(b'SLM(0) \r')
ser.write(b'MV \r')                             # Puts motor in velocity mode
#ser.write(b'MT \r')
                          

injest = int(input("Enter Desired Motor RPM: ")) 
VTcal = (injest/60)*(ENC/SMPL)*65536               # Calculation for VT for Nema 23 and Nema 17 motors (provided by motor guide)
VTcal = str(VTcal)
#VTcal = str(injest)
VTpos = re.sub("X", VTcal, Tval) 
#Tval = re.sub("X", VTcal, Tval) 
VTpos = VTpos.encode()                          # Encodes VTpos string into bytes for use with ser.write command

ser.write(VTpos)                                # Sends target velocity value to motor
ser.write(b'ADT=100 \r')                        # Sends acceleration target velocity to motor
#ser.write(b'MDT \r')                            # Sets motor to trapezoidal commutation mode
ser.write(b'G \r')                              # Begins move
time.sleep(10)                                   # Waits 4 seconds
ser.write(b'X \r') 
time.sleep(1)
ser.write(b'Z \r')

ser.close()
print('End of Test')                            # Notifies user of end of rpm test

# Max torque with 90degree: 25000


