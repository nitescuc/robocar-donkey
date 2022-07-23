import numpy as np
import cv2


class CameraBenchmark:
    def __init__(self):
        self.images = []
        self.cont_images = []
        self.triggered = False
        self.processed = None
    
    def stamp_image(self, image, value):
        cv2.putText(image, 
            str(value), 
            (10,10), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.5,
            (200, 200, 200),
            1)
        return image
    
    def join_images(self):
        return np.vstack(self.cont_images + self.images)

    def run(self, image, trigger_value):
        image = self.stamp_image(image, trigger_value)
        if trigger_value > 0.2:
            if len(self.images) < 16:
                self.images.append(image)
        else:
            if len(self.images) >= 16:
                self.processed = self.join_images()
                self.images = []
            if len(self.cont_images) >= 4:
                del self.cont_images[0]
            self.cont_images.append(image)
        return self.processed
