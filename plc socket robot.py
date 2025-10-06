import socket
import serial
import time
import math
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

# initialize variables
robotIP = "192.168.1.102"
PRIMARY_PORT = 30001
SECONDARY_PORT = 30002
REALTIME_PORT = 30003

#Setting coordinate, acceleration and velocity as needed
home_pos            = [math.radians(78.09),
                       math.radians(-110.21),
                       math.radians(-127.15),
                       math.radians(-32.61),
                       math.radians(-270),
                       math.radians(86.01)]
coordinate_c1       = [0.32404, 0.42072, 0.13153, 2.063, -2.370, 0]
coordinate_c1_dwn   = [0.32404, 0.42072, 0.10000, 2.063, -2.370, 0]
coordinate_c2       = [0.42870, 0.42072, 0.13153, 2.063, -2.370, 0]
coordinate_c2_dwn   = [0.42870, 0.42072, 0.10000, 2.063, -2.370, 0]
coordinate_c3       = [0.51854, 0.42072, 0.13153, 2.063, -2.370, 0]
coordinate_a1       = [0.58242, 0.42072, 0.13153, 2.063,-2.370, 0]
coordinate_a2       = [0.58242, 0.42072, 0.13153, 2.063,-2.370, 0]
acc = 2 #acceleration
vel = 2 #velocity

# Creates new line
new_line = "\n"

def send_urscript_command(command: str):
    """
    This function takes the URScript command defined above, 
    connects to the robot server, and sends 
    the command to the specified port to be executed by the robot.

    Args:
        command (str): URScript command
        
    Returns: 
        None
    """
    try:
        # Create a socket connection with the robot IP and port number defined above
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((robotIP, PRIMARY_PORT))

        # Appends new line to the URScript command (the command will not execute without this)
        command = command+new_line
        print("Sent :", command)
        
        # Send the command
        s.sendall(command.encode('utf-8'))
        
        # Close the connection
        s.close()

    except Exception as e:
        print(f"An error occurred: {e}")

send_urscript_command(f"movej({str(home_pos)}, a={acc}, v={vel})")
send_urscript_command(f"set_digital_out(1, False)")
flag = [0,0]

while True:
    try:
        serPort.write(cmd_.encode("utf-8"))
        data = str()
        if serPort.in_waiting:
            ret = serPort.readline()
            data = ret.decode('ascii')
            start = data.index( '\x02' ) + len( '\x02' )
            end = data.index( '\x03', start )
            data = data[start:end]
            print(f"IR1 = {data[5]}, IR2 = {data[6]}, IR3 = {data[7]}")

            ir = data

            if int(ir[5]) and not flag[0]:
                flag[0] = 1
                print("Sensor 1 on")
                send_urscript_command(f"movel(p{str(coordinate_c1)}, a={acc}, v={vel})")
                send_urscript_command(f"movel(p{str(coordinate_c1_dwn)}, a={acc}, v={vel})")
                send_urscript_command(f"set_digital_out(1, True)")
                send_urscript_command(f"movel(p{str(coordinate_c1)}, a={acc}, v={vel})")
                send_urscript_command(f"movel(p{str(coordinate_a1)}, a={acc}, v={vel})")
                send_urscript_command(f"set_digital_out(1, True)")
                send_urscript_command(f"movej({str(home_pos)}, a={acc}, v={vel})")
                print("C1 Move Finished")
            elif int(ir[6]) and not flag[1]:
                flag[1] = 1
                print("Sensor 2 on")
                send_urscript_command(f"movel(p{str(coordinate_c2)}, a={acc}, v={vel})")
                send_urscript_command(f"movel(p{str(coordinate_c2_dwn)}, a={acc}, v={vel})")
                send_urscript_command(f"set_digital_out(1, True)")
                send_urscript_command(f"movel(p{str(coordinate_c2)}, a={acc}, v={vel})")
                send_urscript_command(f"movel(p{str(coordinate_a2)}, a={acc}, v={vel})")
                send_urscript_command(f"set_digital_out(1, True)")
                send_urscript_command(f"movej({str(home_pos)}, a={acc}, v={vel})")
                print("C2 Move Finished")
            elif not int(ir[5]):                
                flag[0] = 0
                print("Sensor 1 off")
            elif not int(ir[6]):
                flag[1] = 0
                print("Sensor 2 off")
            elif int(ir[5]) and int(ir[6]):
                print("Both sensor on")
                
        time.sleep(1)
    except Exception as e:
        print(e)
        break