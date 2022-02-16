from .inference import prediction
from fastapi import FastAPI
from .schema import Health, Predictions, Inference
from google.cloud import storage

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
    results = prediction(data)
    print(results)
    return Predictions(predictions=results)
