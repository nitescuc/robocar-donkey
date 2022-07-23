import numpy as np
import cv2


class CameraBenchmark:
    def __init__(self):
        self.images = []
        self.triggered = False
        self.processed = None
    
    def stamp_image(self, image, value):
        cv2.putText(image, 
            str(value), 
            (10,10), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.5,
            (57, 255, 20),
            1)
        return image
    
    def join_images(self):
        return np.reshape(np.array(self.images), (16*240, 16*120))

    def run(self, image, trigger_value):
        if trigger_value > 0.5 and len(self.images) < 16:
            self.images.append(self.stamp_image(image, trigger_value))
        else:
            self.processed = self.join_images()
            self.images = []
        return self.processed
