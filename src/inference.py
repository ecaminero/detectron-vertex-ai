import os
from faulthandler import disable
from tqdm import tqdm
from . import gcs
from .schema import Inference
from .utils import get_img_name

import multiprocessing as mp
# Detectron2
from pipeline.capture_images import CaptureImages
from pipeline.capture_image import CaptureImage
from pipeline.predict import Predict
from pipeline.async_predict import AsyncPredict
from pipeline.separate_background import SeparateBackground
from pipeline.annotate_image import AnnotateImage
from pipeline.save_image_gcs import SaveImage
from pipeline.utils import detectron
from .schema import Prediction

def prediction(data: Inference):

    num_gpu = 1
    num_cpu = 3
    single_process = False
    config_opts = []
    disable_progress = False
    instances = data.instances
    parameters = data.parameters
    predictions = []

    for image in instances:
        if not gcs.is_blob(image.bucket, image.image_url):
            continue

        image_url = gcs.get_blob(image.bucket, image.image_url)
        # TODO: Check runing multiples Images without for
        # TODO: prevent image download
        capture_images = CaptureImage(image_url)
        
        cfg = detectron.setup_cfg(
            config_file=parameters.config_file,
            weights_file=parameters.weights_file,
            config_opts=config_opts,
            confidence_threshold=parameters.confidence_threshold,
            cpu=parameters.cpu
        )
        
        if not single_process:
            mp.set_start_method("spawn", force=True)
            predict = AsyncPredict(cfg,
                                num_gpus=num_gpu,
                                num_cpus=num_cpu,
                                queue_size=parameters.queue_size,
                                ordered=False)
        else:
            predict = Predict(cfg)

        if parameters.separate_background:
            separate_background = SeparateBackground("vis_image")
            annotate_image = None
        else:
            separate_background = None
            metadata_name = cfg.DATASETS.TEST[0] if len(cfg.DATASETS.TEST) else "__unused"
            annotate_image = AnnotateImage("vis_image", metadata_name)
        
        save_image = SaveImage("vis_image", parameters.output)

        # Create image processing pipeline
        pipeline = (capture_images |
                    predict |
                    separate_background |
                    annotate_image |
                    save_image)

        # Iterate through pipeline
        try:
            for _ in tqdm(pipeline, disable=disable_progress):
                pass
        except StopIteration:
            return
        except KeyboardInterrupt:
            return
        finally:
            # Remove files
            os.remove(image_url)
            
            # Pipeline cleanup
            predictions.append({
                "image": os.path.join(pipeline.path, get_img_name(image_url)),
            })
            if isinstance(predict, AsyncPredict):
                predict.cleanup()
    
    return predictions
