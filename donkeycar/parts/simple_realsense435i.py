from donkeycar.parts.realsense435i import RealSense435i
import cv2
import numpy as np


class SimpleRealsense435i(RealSense435i):
    def __init__(self, resolution=(120, 160), framerate=20, brightness = 0, rotate = 0, enable_rgb=True, enable_depth=False, processor = None):
        super().__init__(enable_rgb=enable_rgb, enable_depth=enable_depth, enable_imu=False, width=424, height=240, channels=3)
        self.resolution = resolution
        self.framerate = framerate
        self.processor = processor
        self.frame = None
        self.color_image = None


    def _poll(self):
        super()._poll()
        frame = np.copy(self.color_image)
        frame = cv2.resize(frame, (self.resolution[1], self.resolution[0]))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.processor != None:
            frame = self.processor.processFrame(frame)
        self.frame = frame
            

    def run_threaded(self):
        return self.frame, self.depth_image


    def apply_config(self, config):
        if self.processor != None:
            self.processor.apply_config(config)
