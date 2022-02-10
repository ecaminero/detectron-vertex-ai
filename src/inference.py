
from faulthandler import disable
import os
from tqdm import tqdm
import multiprocessing as mp
from .schema import Inference

# Detectron2
from pipeline.capture_images import CaptureImages
from pipeline.capture_image import CaptureImage
from pipeline.predict import Predict
from pipeline.async_predict import AsyncPredict
from pipeline.separate_background import SeparateBackground
from pipeline.annotate_image import AnnotateImage
from pipeline.save_image import SaveImage
from pipeline.utils import detectron

def prediction(data: Inference):
    num_gpu = 1
    num_cpu = 3
    single_process = False
    config_opts = []
    disable_progress = False
    p = dict (
        predictions = [{"value": 999, "location": "location"}],
    )
    instances =  data.instances
    parameters =  data.parameters
    
    # instancesTODO: Check runing multiples Images without for
    capture_images = CaptureImage(instances[0].image_url)

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
        # Pipeline cleanup
        if isinstance(predict, AsyncPredict):
            predict.cleanup()
    
    return p
