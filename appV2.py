import URBasic, URBasic.robotModel, URBasic.urScriptExt
import serial
import time
import cv2
import torch
import csv
import pathlib
import socket
import math
from LRC_checksum_calculator import *
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
# Load your pre-trained model (replace with the correct path to your model)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='object-detection-ultralytics-packed-final/models/exp8/weights/best.pt')

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

# Initialize video capture for real-time detection (0 for webcam, or use a video file path)
cap = cv2.VideoCapture(0)

frame_number = 0

# UR Robot details
# ur_robot_ip = '192.168.1.100'  # Replace with your UR Robot's IP address
# ur_robot_port = 30002  # Replace with your UR Robot's port

#ur_robot_ip = 'localhost'  # Replace with your UR Robot's IP address
#ur_robot_port = 65432  # Replace with your UR Robot's port
# Create a socket object
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
coordinate_c2       = [0.42870, 0.42072, 0.13153, 2.068, -2.370, 0]
coordinate_c2_dwn   = [0.42870, 0.42072, 0.10000, 2.068, -2.370, 0]
coordinate_c3       = [0.51854, 0.42072, 0.13153, 2.062, -2.370, 0]
coordinate_a1       = [0.58242, 0.42072, 0.13153, 20.063,-2.370, 0]
coordinate_a2       = [0.58242, 0.42072, 0.13153, 20.063,-2.370, 0]
acc = 2 #acceleration
vel = 2 #velocity

#top corner table coordinate
cor_x = 0
cor_y = 0

# Define the focal length and pixel size of the camera
focal_length = 50 * 3.779528  # Replace with the focal length of your camera
pixel_size =  0.9 / 1000000 # Replace with the pixel size of your camera

def calculate_orientation(x, y, z, width, height):
    # Calculate the center of the object
    center_x = x + width / 2
    center_y = y + height / 2

    # Calculate the orientation of the object
    rx = math.atan2(height, width)
    ry = math.atan2(center_y, center_x)
    rz = math.atan2(z, math.sqrt(center_x**2 + center_y**2))

    return rx, ry, rz

with open('detected_coordinates.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row in the CSV
    csvwriter.writerow(['Frame', 'Object', 'X', 'Y'])
    rob.movej(q=home_pos,a=acc,v=vel)
    rob.set_standard_digital_out(1, False)
    while cap.isOpened():
        serPort.write(cmd_.encode("utf-8"))
        if serPort.in_waiting:
            ret = serPort.readline()
            data = ret.decode('ascii')
            start = data.index( '\x02' ) + len( '\x02' )
            end = data.index( '\x03', start )
            data = data[start:end]
            print(f"IR1 = {data[5]}, IR2 = {data[6]}, IR3 = {data[7]}")
            if data[5]:
                rob.movel(coordinate_c1,acc,vel)
                rob.movel(coordinate_c1_dwn,acc,vel)
                rob.set_standard_digital_out(1, True)
                rob.movel(coordinate_c1,acc,vel)
                rob.movel(coordinate_a1,acc,vel)
                rob.set_standard_digital_out(1, False)
                rob.movej(home_pos,acc,vel)
                rob.stopl(acc)
            elif data[6]:
                rob.movel(coordinate_c2,acc,vel)
                rob.movel(coordinate_c2_dwn,acc,vel)
                rob.set_standard_digital_out(1, True)
                rob.movel(coordinate_c2,acc,vel)
                rob.movel(coordinate_a2,acc,vel)
                rob.set_standard_digital_out(1, False)
                rob.movej(home_pos,acc,vel)
                rob.stopl(acc)

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Perform inference on the frame
        results = model(frame)
        
        # Loop through the detected objects in the frame
        for detection in results.xyxy:  # xyxy format: [x1, y1, x2, y2, confidence, class]
            if not detection.any() or len(detection) < 1:
                print("not detected")
                cv2.imshow('Object Detection', frame)   
                continue
            if(len(detection[0]) < 6):
                print("not detected")
                cv2.imshow('Object Detection', frame)
                continue
            x1, y1, x2, y2, conf, cls = detection[0].tolist()
            # Calculate the center of the bounding box
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            # Estimate the z position using the object size and aspect ratio
            width = x2 - x1
            height = y2 - y1
            aspect_ratio = width / height
            z = (width / aspect_ratio) * focal_length / (width * pixel_size)
            z = z / 1000000

            # rx, ry, rz = calculate_orientation(x1, y1, z, width, height)
            # Draw bounding box on the frame
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            
            # Add class label to the bounding box
            cv2.putText(frame, f'Class: {int(cls)}', (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Add x, y, z coordinates to the bounding box
            cv2.putText(frame, f'({int(center_x)}, {int(center_y)}, {z:.2f})', (int(x1), int(y1 - 25)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Add rx, ry, rz coordinates to the bounding box
            # cv2.putText(frame, f'(rx: {rx:.2f}, ry: {ry:.2f}, rz: {rz:.2f})', (int(x1), int(y1 - 50)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            print(f'writing {frame_number}, {int(cls)} {center_x} {center_y} {z}')
            if detection.any() and len(detection[0]) >= 6:
                coor_x = center_x + cor_x
                coor_y = center_y + cor_y
                rob.movel([coor_x,coor_y,0.13153,2.063, -2.370, 0], acc, vel)
                rob.rg2_gripper(target_width=100, target_force=40)
                rob.movel([coor_x,coor_y,0.10000,2.063, -2.370, 0], acc, vel) #down for pick, please setting
                rob.rg2_gripper(target_width=50, target_force=40)
                rob.set_standard_digital_out(1, True)
                rob.movel([coor_x,coor_y,0.13153,2.063, -2.370, 0], acc, vel)
                rob.movel(coordinate_c3,acc,vel)
                rob.rg2_gripper(target_width=100, target_force=40)
                rob.movej(home_pos,acc,vel)
                rob.stopj(acc)
                # Send the coordinates to the server
                
            # Save frame number, object class, and coordinates to the CSV file
            csvwriter.writerow([frame_number, int(cls), center_x, center_y])
            csvfile.flush()
            # Wait for a short period before sending the next coordinate
            time.sleep(0.01)
        
        # Display the frame with bounding boxes
        cv2.imshow('Object Detection', frame)
        # Optional: Display the frame with bounding boxes (for visualization)
        # This will display the frame with detections
        
        # Increment the frame number
        frame_number += 1
        
        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()