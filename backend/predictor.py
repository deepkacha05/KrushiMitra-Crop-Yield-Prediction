"""
backend/predictor.py

Production ML backend for KrushiMitra crop yield prediction.

Responsibilities:
    - Load the trained model and preprocessor artifacts from disk (via joblib).
    - Provide a strict prediction pipeline: preprocessor.transform() -> model.predict().
    - Surface clear, actionable errors if artifacts are missing or malformed.

No mock data, no fallback/random predictions. If the model or preprocessor
cannot be loaded, or the prediction pipeline fails, an exception is raised
so the calling UI layer can handle it explicitly.
"""

import os
import joblib
import pandas as pd

# ==========================================
# PATH CONFIGURATION
# ==========================================
# Resolve paths relative to the project root (one level up from backend/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODELS_DIR, "model.pkl")
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "preprocessor.pkl")

# Feature columns expected by the preprocessor, in the exact order the
# preprocessing pipeline was fit on. Must match training-time schema.
FEATURE_COLUMNS = [
    "State",
    "District",
    "Crop",
    "Season",
    "Crop_Year",
    "Area",
]


class ModelLoadError(Exception):
    """Raised when the model or preprocessor artifacts cannot be loaded."""
    pass


class PredictionError(Exception):
    """Raised when the prediction pipeline fails on valid, loaded artifacts."""
    pass


def load_ml_assets(model_path: str = MODEL_PATH, preprocessor_path: str = PREPROCESSOR_PATH):
    """
    Load the trained model and preprocessor from disk using joblib.

    Args:
        model_path: Path to the serialized model (model.pkl).
        preprocessor_path: Path to the serialized preprocessor (preprocessor.pkl).

    Returns:
        (model, preprocessor) tuple.

    Raises:
        ModelLoadError: If either artifact is missing or fails to load.
    """
    if not os.path.exists(model_path):
        raise ModelLoadError(
            f"Model file not found at '{model_path}'. "
            f"Ensure 'model.pkl' is placed inside the 'models' directory."
        )

    if not os.path.exists(preprocessor_path):
        raise ModelLoadError(
            f"Preprocessor file not found at '{preprocessor_path}'. "
            f"Ensure 'preprocessor.pkl' is placed inside the 'models' directory."
        )

    try:
        model = joblib.load(model_path)
    except Exception as e:
        raise ModelLoadError(f"Failed to load model from '{model_path}': {e}") from e

    try:
        preprocessor = joblib.load(preprocessor_path)
    except Exception as e:
        raise ModelLoadError(f"Failed to load preprocessor from '{preprocessor_path}': {e}") from e

    return model, preprocessor


def _validate_input(input_data: dict) -> None:
    """
    Validate that the input dictionary contains all required feature columns.

    Args:
        input_data: Dictionary of feature name -> value.

    Raises:
        PredictionError: If required fields are missing.
    """
    missing = [col for col in FEATURE_COLUMNS if col not in input_data]
    if missing:
        raise PredictionError(
            f"Missing required input fields for prediction: {missing}"
        )


def make_prediction(model, preprocessor, input_data: dict) -> float:
    """
    Execute the strict prediction pipeline:
        1. Build a single-row DataFrame from input_data.
        2. Transform it using the fitted preprocessor.
        3. Predict the yield using the trained model.

    Args:
        model: The trained model object (must implement .predict()).
        preprocessor: The fitted preprocessor (must implement .transform()).
        input_data: Dict with keys matching FEATURE_COLUMNS:
            {
                "State": str,
                "District": str,
                "Crop": str,
                "Season": str,
                "Crop_Year": int,
                "Area": float,
            }

    Returns:
        The predicted yield as a float.

    Raises:
        PredictionError: If validation fails or any pipeline step raises.
    """
    if model is None or preprocessor is None:
        raise PredictionError("Model or preprocessor is not loaded.")

    _validate_input(input_data)

    # Build the DataFrame in the exact column order the preprocessor expects
    input_df = pd.DataFrame([input_data], columns=FEATURE_COLUMNS)

    try:
        processed_features = preprocessor.transform(input_df)
    except Exception as e:
        raise PredictionError(f"Preprocessing failed: {e}") from e

    try:
        prediction = model.predict(processed_features)
    except Exception as e:
        raise PredictionError(f"Model prediction failed: {e}") from e

    if prediction is None or len(prediction) == 0:
        raise PredictionError("Model returned an empty prediction result.")

    return float(prediction[0])
