import serial
import time
from LRC_checksum_calculator import *

# Initialize serial comm
serPort = serial.Serial("COM2",      #port
                    9600,              #baudrate
                    serial.SEVENBITS,   #bytesize
                    serial.PARITY_EVEN,  #parity
                    serial.STOPBITS_ONE, #,#stop bit
                    0,                  #timeout
                    False,              #xonxoff
                    False,              #rtscts
                    0,                  #write_timeout
                    False,              #dsrdtr
                    None,               #inter byte timeout
                    None                #exclusive
                    )

cmd = '014403X0001' #command for read X1~X3
chk = LRC_calc(cmd)
cmd_ = '\x02' + cmd + (str(chk)).upper() + '\x03'

ir1, ir2, ir3 = 0,0,0

while True:
    try:
        serPort.write(cmd_.encode("utf-8"))
        if serPort.in_waiting:
            ret = serPort.readline()
            data = ret.decode('ascii')
            start = data.index( '\x02' ) + len( '\x02' )
            end = data.index( '\x03', start )
            data = data[start:end]
            print(f"IR1 = {data[5]}, IR2 = {data[6]}, IR3 = {data[7]}")
            time.sleep(1)
    except Exception as e:
        print(e)
        break
serPort.close()    