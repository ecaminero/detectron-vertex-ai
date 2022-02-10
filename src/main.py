from .inference import prediction
from urllib import request
from fastapi import FastAPI
from .schema import Health, Predictions, Inference

app = FastAPI()

@app.get("/health", response_model=Health)
def health()-> Health:
    """
    HealthCheck.
    """    
    return {"status": "Ok"}


@app.post("/inference", response_model=Predictions,  summary="Execute Inference")
def inference(data: Inference):
    """
    Ejecute inference
    """    
    print(data) 
    result = prediction(data)
    return {}
