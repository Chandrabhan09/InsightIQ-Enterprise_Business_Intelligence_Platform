import os

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from services.profile_service import ProfileService
from services.visualization_service import VisualizationService

router = APIRouter(prefix="/api/visualization", tags=["Visualization"])


# ==========================================================
# Helper Functions
# ==========================================================


def validate_file(filepath: str):
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dataset not found.")


def load_dataframe(filepath: str):
    validate_file(filepath)
    return ProfileService.load_dataframe(filepath)


def validate_column(df, column_name):
    if column_name not in df.columns:
        raise HTTPException(
            status_code=400, detail=f"Column '{column_name}' not found."
        )


def validate_numeric_column(df, column_name):
    validate_column(df, column_name)

    if not df[column_name].dtype.kind in "iuf":
        raise HTTPException(status_code=400, detail=f"'{column_name}' must be numeric.")


def return_image(image_path):
    return FileResponse(path=image_path, media_type="image/png")


# ==========================================================
# HISTOGRAM
# ==========================================================


@router.get("/histogram")
def histogram(filepath: str = Query(...), column_name: str = Query(...)):
    df = load_dataframe(filepath)

    validate_numeric_column(df, column_name)

    image = VisualizationService.histogram(df, column_name)

    return return_image(image)


# ==========================================================
# BAR CHART
# ==========================================================


@router.get("/bar-chart")
def bar_chart(filepath: str = Query(...), column_name: str = Query(...)):
    df = load_dataframe(filepath)

    validate_column(df, column_name)

    image = VisualizationService.bar_chart(df, column_name)

    return return_image(image)


# ==========================================================
# LINE CHART
# ==========================================================


@router.get("/line-chart")
def line_chart(
    filepath: str = Query(...), x_column: str = Query(...), y_column: str = Query(...)
):
    df = load_dataframe(filepath)

    validate_numeric_column(df, y_column)
    validate_column(df, x_column)

    image = VisualizationService.line_chart(df, x_column, y_column)

    return return_image(image)


# ==========================================================
# SCATTER PLOT
# ==========================================================


@router.get("/scatter-plot")
def scatter_plot(
    filepath: str = Query(...), x_column: str = Query(...), y_column: str = Query(...)
):
    df = load_dataframe(filepath)

    validate_numeric_column(df, x_column)
    validate_numeric_column(df, y_column)

    image = VisualizationService.scatter_plot(df, x_column, y_column)

    return return_image(image)


# ==========================================================
# BOX PLOT
# ==========================================================


@router.get("/box-plot")
def box_plot(filepath: str = Query(...), column_name: str = Query(...)):
    df = load_dataframe(filepath)

    validate_numeric_column(df, column_name)

    image = VisualizationService.box_plot(df, column_name)

    return return_image(image)


# ==========================================================
# PIE CHART
# ==========================================================


@router.get("/pie-chart")
def pie_chart(filepath: str = Query(...), column_name: str = Query(...)):
    df = load_dataframe(filepath)

    validate_column(df, column_name)

    image = VisualizationService.pie_chart(df, column_name)

    return return_image(image)


# ==========================================================
# CORRELATION HEATMAP
# ==========================================================


@router.get("/correlation-heatmap")
def correlation_heatmap(filepath: str = Query(...)):
    df = load_dataframe(filepath)

    image = VisualizationService.correlation_heatmap(df)

    return return_image(image)
