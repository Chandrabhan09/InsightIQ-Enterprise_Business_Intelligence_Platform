from fastapi import APIRouter, Query, HTTPException
from services.profile_service import ProfileService
import os

router = APIRouter(prefix="/api/profile", tags=["Data Profiling"])


@router.get("/")
def profile_home():
    return {"message": "Enterprise Data Profiling API is ready."}


@router.get("/summary")
def dataset_summary(filepath: str = Query(..., description="Path of uploaded dataset")):
    """
    Generate a basic summary of a dataset.
    """

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = ProfileService.load_dataframe(filepath)

    summary = ProfileService.dataset_summary(df)

    return summary


@router.get("/missing-values")
def missing_value_report(filepath: str = Query(...)):
    """
    Generate missing value analysis.
    """

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = ProfileService.load_dataframe(filepath)

    report = ProfileService.missing_value_analysis(df)

    return report


@router.get("/statistics")
def statistical_summary(filepath: str = Query(...)):
    """
    Generate statistical summary for numeric columns.
    """

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = ProfileService.load_dataframe(filepath)

    stats = ProfileService.statistical_summary(df)

    return stats


@router.get("/missing-values")
def missing_value_report(filepath: str = Query(...)):
    """
    Generate missing value analysis.
    """

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = ProfileService.load_dataframe(filepath)

    report = ProfileService.missing_value_analysis(df)

    return report


@router.get("/duplicates")
def duplicate_report(filepath: str = Query(...)):
    """
    Generate duplicate analysis.
    """

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = ProfileService.load_dataframe(filepath)

    report = ProfileService.duplicate_analysis(df)

    return report


@router.get("/data-types")
def data_type_report(filepath: str = Query(...)):
    """
    Generate data type analysis.
    """

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = ProfileService.load_dataframe(filepath)

    report = ProfileService.data_type_analysis(df)

    return report


@router.get("/correlation")
def correlation_report(filepath: str = Query(...)):
    """
    Generate correlation analysis.
    """

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = ProfileService.load_dataframe(filepath)

    report = ProfileService.correlation_analysis(df)

    return report


@router.get("/outliers")
def outlier_report(filepath: str = Query(...)):
    """
    Generate outlier analysis.
    """

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = ProfileService.load_dataframe(filepath)

    report = ProfileService.outlier_analysis(df)

    return report


@router.get("/business-insights")
def business_insight_report(filepath: str = Query(...)):
    """
    Generate business insights.
    """

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = ProfileService.load_dataframe(filepath)

    report = ProfileService.business_insights(df)

    return report


@router.get("/export-report")
def export_report(filepath: str = Query(...)):
    """
    Export complete profiling report.
    """

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = ProfileService.load_dataframe(filepath)

    report = ProfileService.export_report(df)

    return report
