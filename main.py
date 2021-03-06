# import dependencies
import numpy as np
import pandas as pd
from random import seed
from random import randint
import cv2
import serial
import time
import imutils
from imutils.video import VideoStream

# import from other files
from frame_detection import shot_detect
from calibration import calibrate

# initiate
# set up the serial line
ser = serial.Serial('COM4', 9600) # windows port
# ser = serial .Serial('/dev/cu.usbmodem14201', 9600) # mac port

# seed random number
seed(1)
results = [] # array to store all the results of the session

# activate video
print("[INFO] Starting video stream...")
vs = VideoStream(src=1).start() # src=1 for usb camera
time.sleep(2.0)
print("[INFO] Video Ready")

# calibrate the camera for pixel to cm ratio
cm_per_pixel, x_zero, y_zero = calibrate(vs)

# get target coords from csv
target_coords = pd.read_csv("shot_data.csv")
num_targets = sum(1 for line in target_coords)

while (True):
	# if the `q` key was pressed, break from the loop
    frame = vs.read()
    # cv2.imshow("frame", frame)
    # cv2.waitKey(1)

    shot_result = shot_detect(vs, ser, num_targets, target_coords, cm_per_pixel, x_zero, y_zero)
    results.append(shot_result)
    print("Distance from Target:", shot_result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quitting...")
        break

    if cv2.waitKey(1) & 0xFF == ord('r'):
        print("Results: ", *results, sep = "\n")
        break

    # if cv2.waitKey(1) & 0xFF == ord('w'):
    #     print("Shot")
    #     shot_result = shot_detect(vs, ser, num_targets, target_coords)
    #     results.append(shot_result)
    #     print(shot_result)

print(*results, sep = "\n")
cv2.destroyAllWindows()
