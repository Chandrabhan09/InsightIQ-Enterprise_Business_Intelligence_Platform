from fastapi import APIRouter
import os
import pandas as pd
from fastapi import HTTPException, Query
from services.preprocessing_service import PreprocessingService

router = APIRouter(prefix="/api/preprocessing", tags=["Data Preprocessing"])


@router.get("/")
def home():
    """
    Base endpoint.
    """
    return PreprocessingService.home()


@router.get("/health")
def health():
    """
    Health check.
    """
    return PreprocessingService.health()


@router.get("/missing-values")
def handle_missing_values(filepath: str = Query(...), strategy: str = Query("mean")):
    """
    Handle missing values.
    """

    if not os.path.exists(filepath):

        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = pd.read_csv(filepath)

    try:

        return PreprocessingService.handle_missing_values(df, strategy)

    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))


@router.get("/treat-outliers")
def treat_outliers(filepath: str = Query(...)):
    """
    Detect and remove outliers.
    """

    if not os.path.exists(filepath):

        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = pd.read_csv(filepath)

    return PreprocessingService.treat_outliers(df)


@router.get("/encode-categorical")
def encode_categorical(filepath: str = Query(...), strategy: str = Query("label")):
    """
    Encode categorical variables.
    """

    if not os.path.exists(filepath):

        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = pd.read_csv(filepath)

    try:

        return PreprocessingService.encode_categorical(df, strategy)

    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))


@router.get("/scale-features")
def scale_features(filepath: str = Query(...), strategy: str = Query("standard")):
    """
    Scale numerical features.
    """

    if not os.path.exists(filepath):

        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = pd.read_csv(filepath)

    try:

        return PreprocessingService.scale_features(df, strategy)

    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))


@router.get("/feature-engineering")
def feature_engineering(filepath: str = Query(...)):
    """
    Perform feature engineering.
    """

    if not os.path.exists(filepath):

        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = pd.read_csv(filepath)

    try:

        return PreprocessingService.feature_engineering(df)

    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))


@router.get("/feature-selection")
def feature_selection(
    filepath: str = Query(...), target_column: str = Query(...), k: int = Query(5)
):
    """
    Select important features.
    """

    if not os.path.exists(filepath):

        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = pd.read_csv(filepath)

    try:

        return PreprocessingService.feature_selection(df, target_column, k)

    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))


@router.get("/split-dataset")
def split_dataset(
    filepath: str = Query(...),
    target_column: str = Query(...),
    test_size: float = Query(0.2),
    random_state: int = Query(42),
):
    """
    Split dataset into train and test sets.
    """

    if not os.path.exists(filepath):

        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = pd.read_csv(filepath)

    try:

        return PreprocessingService.split_dataset(
            df, target_column, test_size, random_state
        )

    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pipeline")
def preprocessing_pipeline(filepath: str = Query(...)):
    """
    Execute complete preprocessing pipeline.
    """

    if not os.path.exists(filepath):

        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = pd.read_csv(filepath)

    return PreprocessingService.preprocessing_pipeline(df)


@router.get("/export-processed")
def export_processed_dataset(filepath: str = Query(...)):
    """
    Export processed dataset.
    """

    if not os.path.exists(filepath):

        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = pd.read_csv(filepath)

    return PreprocessingService.export_processed_dataset(df)
