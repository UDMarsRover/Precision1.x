import serial
import time

ser = serial.Serial("/dev/cu.usbserial-AR0K85IE",57600)
time.sleep(2)

ser.flushInput()

while True:
    print("loop")
    if (ser.inWaiting() > 0):
        try:
            ser_bytes = ser.read_until()
            print(ser_bytes)#format(ser_bytes, 'x'))
            #print(str(ser_bytes))
        except Exception as e:
            print(e)
            pass
#    try:
#        ser_bytes = ser.read(1)#perhaps should be empty param?
#        #decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
#        print(format(ser_bytes, 'x'))#print(decoded_bytes)
#    except:
#        print("interrupt")
#        #break
    time.sleep(1)
