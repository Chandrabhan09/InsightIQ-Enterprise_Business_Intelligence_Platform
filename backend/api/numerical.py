import os

import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from services.numerical_service import NumericalService

router = APIRouter(
    prefix="/api/numerical",
    tags=["Numerical Computing"]
)


@router.get("/")
def numerical_home():
    return NumericalService.health_check()


@router.get("/summary")
def numerical_summary(
    filepath: str = Query(...),
    column_name: str = Query(...)
):
    """
    Generate numerical summary using NumPy.
    """

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    try:
        df = pd.read_csv(filepath)

        report = NumericalService.numerical_summary(
            df,
            column_name
        )

        return report

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/percentiles")
def percentile_summary(
    filepath: str = Query(...),
    column_name: str = Query(...)
):
    """
    Generate percentile summary.
    """

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    try:
        df = pd.read_csv(filepath)

        report = NumericalService.percentile_summary(
            df,
            column_name
        )

        return report

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )  

@router.get("/advanced-statistics")
def advanced_statistics(
    filepath: str = Query(...),
    column_name: str = Query(...)
):
    """
    Generate advanced statistical metrics.
    """

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    try:
        df = pd.read_csv(filepath)

        report = NumericalService.advanced_statistics(
            df,
            column_name
        )

        return report

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )  
       
@router.get("/normalize")
def normalize_data(
    filepath: str = Query(...),
    column_name: str = Query(...),
    method: str = Query("minmax")
):
    """
    Normalize numerical data.
    """

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    try:

        df = pd.read_csv(filepath)

        report = NumericalService.normalize_data(
            df,
            column_name,
            method
        )

        return report

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/standardize")
def standardize_data(
    filepath: str = Query(...),
    column_name: str = Query(...)
):
    """
    Standardize numerical data using Z-score.
    """

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    try:

        df = pd.read_csv(filepath)

        report = NumericalService.standardize_data(
            df,
            column_name
        )

        return report

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/matrix")
def matrix_operations(
    filepath: str = Query(...)
):
    """
    Enterprise matrix operations.
    """

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    try:

        df = pd.read_csv(filepath)

        report = NumericalService.matrix_operations(df)

        return report

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/linear-algebra")
def linear_algebra(
    filepath: str = Query(...)
):
    """
    Enterprise Linear Algebra Analytics.
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    try:

        df = pd.read_csv(filepath)

        report = NumericalService.linear_algebra_analysis(df)

        return report

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/performance")
def performance_benchmark(
    filepath: str = Query(...),
    column_name: str = Query(...)
):
    """
    Compare NumPy and Pandas performance.
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    try:

        df = pd.read_csv(filepath)

        report = NumericalService.performance_benchmark(
            df,
            column_name
        )

        return report

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/report")
def generate_numerical_report(
    filepath: str = Query(...),
    column_name: str = Query(...)
):
    """
    Generate complete numerical analytics report.
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    try:

        df = pd.read_csv(filepath)

        report = NumericalService.generate_numerical_report(
            df,
            column_name
        )

        return report

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/visualize")
def visualize(
    filepath: str = Query(...),
    column_name: str = Query(...)
):
    """
    Generate numerical visualization charts.
    """

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    try:

        df = pd.read_csv(filepath)

        report = NumericalService.generate_visualizations(
            df,
            column_name
        )

        return report

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )