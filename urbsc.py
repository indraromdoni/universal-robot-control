import URBasic, URBasic.connectionState, URBasic.robotConnector, URBasic.robotModel, URBasic.urScriptExt
import math
import time
import math3d as m3d

ROBOT_IP = '192.168.159.217'
ACCELERATION = 2 # Robot acceleration value
VELOCITY = 2  # Robot speed value

# The Joint position the robot starts at
robot_startposition = (math.radians(0),
                    math.radians(-45),
                    math.radians(-90),
                    math.radians(-135),
                    math.radians(90),
                    math.radians(0))

c1 = (math.radians(-24.97),
    math.radians(-114.45),
    math.radians(-84.60),
    math.radians(-70.95),
    math.radians(90),
    math.radians(-24.97))
c1_take = (math.radians(-24.97),
        math.radians(-120.25),
        math.radians(-91.77),
        math.radians(-57.97),
        math.radians(90),
        math.radians(-24.97))

c2 = (math.radians(0),
    math.radians(-45),
    math.radians(-90),
    math.radians(-135),
    math.radians(90),
    math.radians(0))

c3 = [0.45060, 0.33364, 0.27690, 2.221, -2.221, 0]

area_a1 = (math.radians(3.01),
        math.radians(-106.43),
        math.radians(-112.88),
        math.radians(-50.68),
        math.radians(90),
        math.radians(3.01))
# initialise robot with URBasic
print("initialising robot")
robotModel = URBasic.robotModel.RobotModel()
robot = URBasic.urScriptExt.UrScriptExt(host=ROBOT_IP,robotModel=robotModel)

robot.reset_error()
print("robot initialised")
time.sleep(1)
res = robot.get_actual_joint_positions()
print(res)
position = robot.get_actual_tcp_pose()
print("origin =", position)
# Move Robot to the midpoint of the lookplane
robot.set_configurable_digital_out(0, False)
robot.movej(q=robot_startposition, a= ACCELERATION, v= VELOCITY)
robot.movej(q=c1, a= ACCELERATION, v= VELOCITY)
robot.movej(q=c1_take, a= ACCELERATION, v= VELOCITY)
robot.set_configurable_digital_out(0, True)
robot.movej(q=c1, a= ACCELERATION, v= VELOCITY)
robot.movej(q=area_a1, a= ACCELERATION, v= VELOCITY)
robot.set_configurable_digital_out(0, False)
robot.movej(q=robot_startposition, a= ACCELERATION, v= VELOCITY)

area_random = [0.45061, -0.133, 0.2769, 2.221, -2.221, 0]
robot.movel(pose=area_random, a=ACCELERATION, v=VELOCITY)
robot.set_configurable_digital_out(0, False)
area_random[2] -= 0.05
robot.movel(pose=area_random, a=ACCELERATION, v=VELOCITY)
robot.set_configurable_digital_out(0, True)
area_random[2] += 0.05
robot.movel(pose=area_random, a=ACCELERATION, v=VELOCITY)
robot.movel(pose=c3, a=ACCELERATION, v=VELOCITY)
c3[2] -= 0.05
robot.movel(pose=c3, a=ACCELERATION, v=VELOCITY)
robot.set_configurable_digital_out(0, False)
c3[2] += 0.05
robot.movel(pose=c3, a=ACCELERATION, v=VELOCITY)
robot.movej(q=robot_startposition, a= ACCELERATION, v= VELOCITY)
robot.close()
'''
robot.init_realtime_control()  # starts the realtime control loop on the Universal-Robot Controller
time.sleep(1) # just a short wait to make sure everything is initialised'''