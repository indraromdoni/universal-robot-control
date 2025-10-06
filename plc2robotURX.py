import urx
import math
from urx import RobotException
from time import sleep

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
a = 2
v = 2

rob = urx.Robot("192.168.1.102")
rob.set_tcp((0, 0, 0.1, 0, 0, 0))
rob.set_payload(2, (0, 0, 0.1))
sleep(0.2)  #leave some time to robot to process the setup commands
rob.movej(home_pos, a, v, 0, 0)
rob.movel(coordinate_c1, a, v)
rob.movej(home_pos, a, v)
rob.close()