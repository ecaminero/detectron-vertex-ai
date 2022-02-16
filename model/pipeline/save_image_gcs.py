import os
import cv2
from pipeline.pipeline import Pipeline
from google.cloud import storage


class SaveImage(Pipeline):
    """Pipeline task to save images."""

    def __init__(self, src, path, image_ext="jpg", jpg_quality=None, png_compression=None):
        self.src = src
        self.path = path
        self.image_ext = image_ext
        self.jpg_quality = jpg_quality  # 0 - 100 (higher means better). Default is 95.
        self.png_compression = png_compression  # 0 - 9 (higher means a smaller size and longer compression time). Default is 3.
        self.client = storage.Client()
        self.result = None

        super().__init__()

    def map(self, data):
        image = data[self.src]
        image_name = data["name"]
        bucket = None
        tmp_folder = "tmp"
        # Prepare output for image based on image_id
        dirname = self.path
        output = dirname.split("/")

        if len(output[:-1]) > 0:
            bucket = output[2]
            dirname = os.path.join(*output[2:-1])
            tmp_folder = os.path.join("tmp", dirname)

            os.makedirs(tmp_folder, exist_ok=True)

        tmp_file = os.path.join(tmp_folder, image_name)

        if self.image_ext == "jpg":
            cv2.imwrite(tmp_file, image,
                        (cv2.IMWRITE_JPEG_QUALITY, self.jpg_quality) if self.jpg_quality else None)
        elif self.image_ext == "png":
            cv2.imwrite(tmp_file, image,
                        (cv2.IMWRITE_PNG_COMPRESSION, self.png_compression) if self.png_compression else None)
        else:
            raise Exception("Unsupported image format")
        
        # Instantiates a client
        remote_path = os.path.join(*output[3:-1], image_name)
        bucket = self.client.get_bucket(bucket)
        blob = bucket.blob(remote_path)
        self.result = blob.upload_from_filename(filename=tmp_file)
        # Remove files
        os.remove(tmp_file)
        return data
