from realsense435i import RealSense435i


class SimpleRealsense435i(RealSense435i):
    def __init__(self, resolution=(120, 160), framerate=20, brightness = 0, rotate = 0, processor = None):
        super().__init__(enable_rgb=True, enable_depth=True, enable_imu=False, width=resolution[1], height=resolution[0], channels=1)
        self.resolution = resolution
        self.framerate = framerate
        self.processor = processor
        self.mix_depth = mix_depth


    def _poll(self):
        super()._poll()
        if self.processor != None:
            self.color_image = self.processor.processFrame(self.color_image)
            

    def run_threaded(self):
        return self.color_image, self.depth_image


    def apply_config(self, config):
        if self.processor != None:
            self.processor.apply_config(config)
