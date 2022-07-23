""" 
CAR CONFIG 

This file is read by your car application's manage.py script to change the car
performance. 

EXMAPLE
-----------
import dk
cfg = dk.load_config(config_path='~/d2/config.py')
print(cfg.CAMERA_RESOLUTION)

"""


import os

#PATHS
CAR_PATH = PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(CAR_PATH, 'data')
MODELS_PATH = os.path.join(CAR_PATH, 'models')

#VEHICLE
DRIVE_LOOP_HZ = 60
MAX_LOOPS = 100000

#CAMERA
CAMERA_RESOLUTION = (120, 160) #(height, width)
CAMERA_FRAMERATE = DRIVE_LOOP_HZ
CAMERA_BRIGHTNESS = 0
CAMERA_TRIM_BOTTOM = (95,120)
CAMERA_ENABLE_DEPTH = True

SLOW_THROTTLE = 0.25
MEDIUM_THROTTLE = 0.40
FAST_THROTTLE = 0.75

#TRAINING
BATCH_SIZE = 128
TRAIN_TEST_SPLIT = 0.8
