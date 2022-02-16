import cv2
import os
from pipeline.pipeline import Pipeline


class CaptureImage(Pipeline):
    """Pipeline task to capture single image file"""

    def __init__(self, src):
        self.src = src

        super().__init__()

    def generator(self):
        """Yields the image content and metadata."""

        image = cv2.imread(self.src)

        data = {
            "name": os.path.basename(self.src),
            "image_id": self.src,
            "image": image
        }

        if self.filter(data):
            yield self.map(data)
