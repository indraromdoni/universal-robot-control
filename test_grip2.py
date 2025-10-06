import URBasic, URBasic.robotModel, URBasic.urScriptExt
import time

ROBOT_IP = '192.168.1.102'

# initialise robot with URBasic
print("initialising robot")
robotModel = URBasic.robotModel.RobotModel()
robot = URBasic.urScriptExt.UrScriptExt(host=ROBOT_IP,robotModel=robotModel)

robot.reset_error()
print("robot initialised")
time.sleep(1)
robot.rg2_gripper(50, 40)
time.sleep(3)
robot.rg2_gripper(0, 40)
time.sleep(3)
robot.rg2_gripper(50, 40)
robot.close()