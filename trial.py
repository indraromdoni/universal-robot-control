import URBasic, URBasic.connectionState, URBasic.robotConnector, URBasic.robotModel, URBasic.urScriptExt
import math
import time
import math3d as m3d

ROBOT_IP = '192.168.159.217'
ACCELERATION = 2 # Robot acceleration value
VELOCITY = 2  # Robot speed value

# The Joint position the robot starts at
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
coordinate_a1       = [0.58242, 0.42072, 0.13153, 2.063, -2.370, 0]
coordinate_a2       = [0.58242, 0.62072, 0.13153, 2.063, -2.370, 0]
acc = 0.05 #acceleration
vel = 0.05 #velocity

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
robot.movej(q=home_pos, a= ACCELERATION, v= VELOCITY)
robot.movel(pose=coordinate_c1, a= ACCELERATION, v= VELOCITY)
robot.movel(pose=coordinate_c1_dwn, a= ACCELERATION, v= VELOCITY)
robot.set_configurable_digital_out(0, True)
robot.movel(pose=coordinate_c1, a= ACCELERATION, v= VELOCITY)
robot.movel(pose=coordinate_a1, a= ACCELERATION, v= VELOCITY)
robot.set_configurable_digital_out(0, False)
robot.movej(q=home_pos, a= ACCELERATION, v= VELOCITY)

robot.movel(pose=coordinate_a2, a=ACCELERATION, v=VELOCITY)
robot.set_configurable_digital_out(0, False)
robot.movel(pose=coordinate_a2, a=ACCELERATION, v=VELOCITY)
robot.set_configurable_digital_out(0, True)
robot.movel(pose=coordinate_a2, a=ACCELERATION, v=VELOCITY)
robot.movel(pose=coordinate_c3, a=ACCELERATION, v=VELOCITY)
coordinate_c3[2] -= 0.05
robot.movel(pose=coordinate_c3, a=ACCELERATION, v=VELOCITY)
robot.set_configurable_digital_out(0, False)
coordinate_c3[2] += 0.05
robot.movel(pose=coordinate_c3, a=ACCELERATION, v=VELOCITY)
robot.movej(q=home_pos, a= ACCELERATION, v= VELOCITY)
robot.close()
'''
robot.init_realtime_control()  # starts the realtime control loop on the Universal-Robot Controller
time.sleep(1) # just a short wait to make sure everything is initialised'''