import os

import pandas as pd

from fastapi import APIRouter, HTTPException, Query

from services.eda_service import EDAService

router = APIRouter(
    prefix="/api/eda",
    tags=["Exploratory Data Analysis"]
)


@router.get("/")
def health_check():
    return EDAService.health_check()


@router.get("/overview")
def dataset_overview(
    filepath: str = Query(...)
):
    """
    Enterprise Dataset Overview
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return EDAService.dataset_overview(df)
@router.get("/missing-analysis")
def missing_analysis(
    filepath: str = Query(...)
):
    """
    Enterprise Missing Value Analysis
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return EDAService.missing_value_analysis(df)

@router.get("/duplicate-analysis")
def duplicate_analysis(
    filepath: str = Query(...)
):
    """
    Enterprise Duplicate Analysis
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return EDAService.duplicate_analysis(df)

@router.get("/column-classification")
def column_classification(
    filepath: str = Query(...)
):
    """
    Enterprise Column Classification
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return EDAService.column_classification(df)

@router.get("/distribution-analysis")
def distribution_analysis(
    filepath: str = Query(...)
):
    """
    Enterprise Distribution Analysis
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return EDAService.distribution_analysis(df)

@router.get("/categorical-analysis")
def categorical_analysis(
    filepath: str = Query(...)
):
    """
    Enterprise Categorical Analysis
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return EDAService.categorical_analysis(df)
@router.get("/correlation-analysis")
def correlation_analysis(
    filepath: str = Query(...)
):
    """
    Enterprise Correlation Analysis
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return EDAService.correlation_analysis(df)

@router.get("/outlier-analysis")
def outlier_analysis(
    filepath: str = Query(...)
):
    """
    Enterprise Outlier Analysis
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return EDAService.outlier_analysis(df)

@router.get("/business-insights")
def business_insights(
    filepath: str = Query(...)
):
    """
    Enterprise Business Insight Generator
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return EDAService.business_insights(df)

@router.get("/export-report")
def export_report(
    filepath: str = Query(...)
):
    """
    Export Complete EDA Report
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return EDAService.export_report(df)