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
robot.set_tool_digital_out(1, True)
time.sleep(3)
robot.set_tool_digital_out(1, False)
time.sleep(3)
robot.set_tool_digital_out(0, True)
time.sleep(3)
robot.set_tool_digital_out(0, False)
robot.close()