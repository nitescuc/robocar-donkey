import numpy as np

STEERING_SAMPLES = 31
THROTTLE_SAMPLES = 15

class ThrottleController():
    def __init__(self, slow_throttle=0.4285, medium_throttle=0.7142, fast_throttle=1):
        self.slow_throttle = slow_throttle
        self.medium_throttle = medium_throttle
        self.fast_throttle = fast_throttle

        self.prev_distance = None

        self.on = True


    def apply_config(self, config):
        if 'slow_throttle' in config:
            self.slow_throttle = config['slow_throttle']
        if 'medium_throttle' in config:
            self.medium_throttle = config['medium_throttle']
        if 'fast_throttle' in config:
            self.fast_throttle = config['fast_throttle']        


    def run(self, angle, throttle, distance_map):
        if angle == None:
            angle = (STEERING_SAMPLES - 1)/2
        if throttle == None:
            throttle = 7
        remap_angle = angle * (2/(STEERING_SAMPLES-1)) - 1
        # remap_throttle = throttle * (2/(THROTTLE_SAMPLES - 1)) - 1
        remap_throttle = 0
        if throttle < 12:
            remap_throttle = self.slow_throttle
        elif throttle > 12:
            remap_throttle = self.fast_throttle
        else:
            remap_throttle = self.medium_throttle

        # ROI
        cropped_map = distance_map[20:100,20:]
        # get closest obstacle
        distance = cropped_map.min()
        if self.prev_distance is None:
            self.prev_distance = distance
        # adjust speed
        if distance < 0.2:
            remap_throttle = 0
        elif distance < 0.5 and distance < self.prev_distance:
            correction = 1 - (self.prev_distance - distance)/self.prev_distance
            remap_throttle = remap_throttle * correction
        self.prev_distance = distance

        return remap_angle, remap_throttle

    def run_threaded(self, angle, throttle):
        pass

    def update(self):
        pass

    def shutdown(self):
        self.on = False
