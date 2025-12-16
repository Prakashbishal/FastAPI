from pathlib import Path
import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI(title="Iris Classifier")

CLASS_NAMES = ["setosa", "versicolor", "virginica"]
MODEL_PATH = Path(r"D:\FastAPI\saved_model_iris.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

class UserInput(BaseModel):
    sepal_length: Annotated[float, Field(..., ge=4.3, le=7.9, description="Sepal length in cm (4.3–7.9)")]
    sepal_width:  Annotated[float, Field(..., ge=2.0, le=4.4, description="Sepal width in cm (2.0–4.4)")]
    petal_length: Annotated[float, Field(..., ge=1.0, le=6.9, description="Petal length in cm (1.0–6.9)")]
    petal_width:  Annotated[float, Field(..., ge=0.1, le=2.5, description="Petal width in cm (0.1–2.5)")]

@app.post("/predict")
def predict_flower(data: UserInput):
    input_df = pd.DataFrame([{
        "sepal length (cm)": data.sepal_length,
        "sepal width (cm)": data.sepal_width,
        "petal length (cm)": data.petal_length,
        "petal width (cm)": data.petal_width,
    }])

    prediction_id = int(model.predict(input_df)[0])
    prediction_name = CLASS_NAMES[prediction_id]

    response = {
        "predicted_category_id": prediction_id,
        "predicted_category_name": prediction_name,
    }

    # Optional: include probabilities if available
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_df)[0]
        response["probabilities"] = {CLASS_NAMES[i]: float(probs[i]) for i in range(len(CLASS_NAMES))}

    return response
