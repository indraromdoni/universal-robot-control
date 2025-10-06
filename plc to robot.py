import URBasic, URBasic.robotModel, URBasic.urScriptExt
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

ur_robot_ip = "192.168.1.102"
robotModel = URBasic.robotModel.RobotModel()
rob = URBasic.urScriptExt.UrScriptExt(host=ur_robot_ip,robotModel=robotModel)

#Setting coordinate, acceleration and velocity as needed
home_pos            = (math.radians(78.09),
                       math.radians(-110.21),
                       math.radians(-127.15),
                       math.radians(-32.61),
                       math.radians(-270),
                       math.radians(86.01))
coordinate_c1       = [0.32404, 0.42072, 0.13153, 2.063, -2.370, 0]
coordinate_c1_dwn   = [0.32404, 0.42072, 0.10000, 2.063, -2.370, 0]
coordinate_c2       = [0.42870, 0.42072, 0.13153, 2.063, -2.370, 0]
coordinate_c2_dwn   = [0.42870, 0.42072, 0.10000, 2.063, -2.370, 0]
coordinate_c3       = [0.51854, 0.42072, 0.13153, 2.063, -2.370, 0]
coordinate_a1       = [0.58242, 0.42072, 0.13153, 2.063,-2.370, 0]
coordinate_a2       = [0.58242, 0.42072, 0.13153, 2.063,-2.370, 0]
acc = 2 #acceleration
vel = 2 #velocity

rob.reset_error()
rob.movej(q=home_pos,a=acc,v=vel)
#rob.set_standard_digital_out(1, False)
rob.rg2_gripper(target_width=100, target_force=40)
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
                rob.movel(coordinate_c1,acc,vel)
                rob.movel(coordinate_c1_dwn,acc,vel)
                #rob.set_standard_digital_out(1, True)
                rob.rg2_gripper(target_width=50, target_force=40)
                rob.set_tool_digital_out(1, True)
                rob.movel(coordinate_c1,acc,vel)
                rob.movel(coordinate_a1,acc,vel)
                #rob.set_standard_digital_out(1, False)
                rob.rg2_gripper(target_width=100, target_force=40)
                rob.movej(home_pos,acc,vel)
                rob.stopj(acc)
                print("C1 Move Finished")
            elif int(ir[6]) and not flag[1]:
                flag[1] = 1
                print("Sensor 2 on")
                rob.movel(coordinate_c2,acc,vel)
                rob.movel(coordinate_c2_dwn,acc,vel)
                #rob.set_standard_digital_out(1, True)
                rob.rg2_gripper(target_width=50, target_force=40)
                rob.movel(coordinate_c2,acc,vel)
                rob.movel(coordinate_a2,acc,vel)
                #rob.set_standard_digital_out(1, False)
                rob.rg2_gripper(target_width=100, target_force=40)
                rob.movej(home_pos,acc,vel)
                rob.stopj(acc)
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
rob.close()