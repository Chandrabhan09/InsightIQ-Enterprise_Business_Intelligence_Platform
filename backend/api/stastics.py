from fastapi import APIRouter, HTTPException, Query
import os
import pandas as pd

from services.statistics_service import StatisticsService

router = APIRouter(
    prefix="/api/statistics",
    tags=["Statistical Analysis"]
)


@router.get("/")
def statistics_home():

    return StatisticsService.health()


@router.get("/descriptive-statistics")
def descriptive_statistics(
    filepath: str = Query(...)
):
    """
    Enterprise Descriptive Statistics
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return StatisticsService.descriptive_statistics(df)


@router.get("/probability-distribution")
def probability_distribution(
    filepath: str = Query(...)
):
    """
    Enterprise Probability Distribution Analysis
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return StatisticsService.probability_distribution(df)

@router.get("/confidence-intervals")
def confidence_intervals(
    filepath: str = Query(...)
):
    """
    Enterprise Confidence Interval Calculator
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return StatisticsService.confidence_intervals(df)

@router.get("/hypothesis-test")
def hypothesis_test(
    filepath: str = Query(...),
    column: str = Query(...),
    hypothesized_mean: float = Query(...)
):
    """
    Enterprise One-Sample Hypothesis Test
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    try:
        return StatisticsService.hypothesis_test(
            df,
            column,
            hypothesized_mean
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/normality-test")
def normality_test(
    filepath: str = Query(...),
    column: str = Query(...)
):
    """
    Enterprise Normality Test
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    try:

        return StatisticsService.normality_test(
            df,
            column
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/anova-test")
def anova_test(
    filepath: str = Query(...),
    numerical_column: str = Query(...),
    group_column: str = Query(...)
):
    """
    Enterprise One-Way ANOVA
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    try:

        return StatisticsService.anova_test(
            df,
            numerical_column,
            group_column
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/chi-square-test")
def chi_square_test(
    filepath: str = Query(...),
    column1: str = Query(...),
    column2: str = Query(...)
):
    """
    Enterprise Chi-Square Test
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    try:

        return StatisticsService.chi_square_test(
            df,
            column1,
            column2
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/correlation-significance")
def correlation_significance(
    filepath: str = Query(...),
    column1: str = Query(...),
    column2: str = Query(...)
):
    """
    Enterprise Correlation Significance Test
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    try:

        return StatisticsService.correlation_significance(
            df,
            column1,
            column2
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/statistical-insights")
def statistical_insights(
    filepath: str = Query(...)
):
    """
    Enterprise Statistical Insight Generator
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return StatisticsService.statistical_insights(df)


@router.get("/export-report")
def export_statistics_report(
    filepath: str = Query(...)
):
    """
    Export Statistical Report
    """

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(filepath)

    return StatisticsService.export_statistics_report(df)