import sys
import time
import socket

STEERING_SAMPLES = 31
THROTTLE_SAMPLES = 15

class UdpActuatorEmitter():
    def __init__(self, remote_addr, remote_port, slow_throttle=0.4285, medium_throttle=0.7142, fast_throttle=1):
        #  Socket to talk to server
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.remote_addr = remote_addr
        self.remote_port = remote_port

        self.slow_throttle = slow_throttle
        self.medium_throttle = medium_throttle
        self.fast_throttle = fast_throttle

        self.on = True


    def apply_config(self, config):
        if 'slow_throttle' in config:
            self.slow_throttle = config['slow_throttle']
        if 'medium_throttle' in config:
            self.medium_throttle = config['medium_throttle']
        if 'fast_throttle' in config:
            self.fast_throttle = config['fast_throttle']


    def run(self, angle, throttle, mode):
        if angle == None:
            angle = (STEERING_SAMPLES - 1)/2
        if throttle == None:
            throttle = 7
        if mode == None:
            mode = 'user'
        remap_angle = angle * (2/(STEERING_SAMPLES-1)) - 1
        # remap_throttle = throttle * (2/(THROTTLE_SAMPLES - 1)) - 1
        remap_throttle = 0
        if throttle < 12:
            remap_throttle = self.slow_throttle
        elif throttle > 12:
            remap_throttle = self.fast_throttle
        else:
            remap_throttle = self.medium_throttle
        bytesToSend = ("{:01.4f};{:01.4f};{}".format(remap_angle, remap_throttle, mode)).encode()
        self.socket.sendto(bytesToSend, (self.remote_addr, self.remote_port))

        return remap_angle, remap_throttle

    def run_threaded(self, angle, throttle, mode):
        pass

    def update(self):
        pass

    def shutdown(self):
        bytesToSend = ("{:01.4f};{:01.4f};{}".format(0, 0, 'user')).encode()
        self.socket.sendto(bytesToSend, (self.remote_addr, self.remote_port))
        # indicate that the thread should be stopped
        self.on = False
        print('stoping UdpActuatorEmitter')
