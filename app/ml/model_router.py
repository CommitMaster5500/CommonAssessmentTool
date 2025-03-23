from fastapi import APIRouter, HTTPException
from typing import List
import os
import shutil
import json

router = APIRouter(prefix="/ml_models", tags=["models"])

# ------------------ Constants ------------------ #
MODEL_DIR = "ml_models"  # Directory where all .pkl models are stored
MODEL_CONFIG = "model_config.json"  # Tracks current model
MODEL_ACTIVE_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")  # Fixed model path used by locked module


# ------------------ Helper Functions ------------------ #
def list_models() -> List[str]:
    """List all available .pkl models in the model directory"""
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    return [f.replace(".pkl", "") for f in os.listdir(MODEL_DIR) if f.endswith(".pkl")]


def get_active_model() -> str:
    """Get the name of the currently active model from config"""
    if not os.path.exists(MODEL_CONFIG):
        raise HTTPException(status_code=404, detail="No active model set.")
    with open(MODEL_CONFIG, "r") as f:
        config = json.load(f)
    return config.get("active_model")


def set_active_model(model_name: str):
    """Set active model by copying it to model.pkl and updating config"""
    available = list_models()
    if model_name not in available:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found.")

    source_path = os.path.join(MODEL_DIR, f"{model_name}.pkl")

    try:
        shutil.copyfile(source_path, MODEL_ACTIVE_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to activate model: {str(e)}")

    with open(MODEL_CONFIG, "w") as f:
        json.dump({"active_model": model_name}, f)


# ------------------ API Endpoints ------------------ #

@router.get("/", response_model=List[str])
def get_model_list():
    """List all available models"""
    return list_models()


@router.get("/active")
def get_active_model_endpoint():
    """Get the name of the current active model"""
    return {"active_model": get_active_model()}


@router.post("/active")
def set_active_model_endpoint(model_name: str):
    """Set the active model and overwrite model.pkl"""
    set_active_model(model_name)
    return {"status": "success", "active_model": model_name}
