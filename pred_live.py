from __future__ import print_function

import time

import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
from keras.utils import CustomObjectScope
from sklearn.model_selection import train_test_split

from data import seed, standardize
from loss import np_dice_coef
from nets.MobileUNet import custom_objects

from imutils.video import VideoStream
import imutils
import time
import cv2

SAVED_MODEL1 = 'artifacts/model.h5'

size = 224

width = size
height = size

x = 40
y = 0

 
# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream().start()
time.sleep(2.0)

with CustomObjectScope(custom_objects()):
    model1 = load_model(SAVED_MODEL1)

# loop over the frames from the video stream
while True:
	frame = vs.read()
        resized = imutils.resize(frame, height=size)

        crop_frame = resized[y:y+height, x:x+width]
        reshaped = crop_frame.reshape(1, size, size, 3).astype(float)

        pred1 = model1.predict(standardize(reshaped)).reshape(size, size)

	# show the frame
	cv2.imshow("Frame", crop_frame)
	cv2.imshow("Segment", pred1)

	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
 
cv2.destroyAllWindows()
vs.stop()



