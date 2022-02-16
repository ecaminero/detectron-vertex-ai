from pydantic import BaseModel, Field
from typing import List, Optional

class Instances(BaseModel):
    image_url: str
    bucket: str

class Parameters(BaseModel):
    output: str
    config_file: Optional[str] = "model/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    weights_file: Optional[str] = None
    confidence_threshold: Optional[float] = 0.5
    cpu: Optional[bool] = False
    single_process: Optional[bool] = False
    queue_size: Optional[bool] = 3
    separate_background: Optional[bool] = False

class Prediction(BaseModel):
    image: str
    
# Schema for API
class Inference(BaseModel):
    instances: List[Instances]
    parameters: Optional[Parameters]


class Predictions(BaseModel):
    predictions: List[Prediction]

class Health(BaseModel):
    status: str