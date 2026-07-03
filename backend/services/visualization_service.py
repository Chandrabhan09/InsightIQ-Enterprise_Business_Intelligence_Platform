import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class VisualizationService:
    """
    Service responsible for generating visualization charts.
    Every function returns the path of the generated image.
    """

    OUTPUT_FOLDER = "output"

    @staticmethod
    def _prepare_output_folder():
        os.makedirs(VisualizationService.OUTPUT_FOLDER, exist_ok=True)

    @staticmethod
    def _save_plot(filename: str):
        VisualizationService._prepare_output_folder()

        output_path = os.path.join(VisualizationService.OUTPUT_FOLDER, filename)

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return output_path

    # ============================================================
    # HISTOGRAM
    # ============================================================

    @staticmethod
    def histogram(df: pd.DataFrame, column_name: str):

        plt.figure(figsize=(8, 5))

        plt.hist(df[column_name], bins=20, edgecolor="black")

        plt.title(f"Histogram of {column_name}")
        plt.xlabel(column_name)
        plt.ylabel("Frequency")

        return VisualizationService._save_plot("histogram.png")

    # ============================================================
    # BAR CHART
    # ============================================================

    @staticmethod
    def bar_chart(df: pd.DataFrame, column_name: str):

        counts = df[column_name].value_counts()

        plt.figure(figsize=(10, 6))

        plt.bar(counts.index.astype(str), counts.values)

        plt.title(f"Bar Chart of {column_name}")
        plt.xlabel(column_name)
        plt.ylabel("Count")

        plt.xticks(rotation=45)

        return VisualizationService._save_plot("bar_chart.png")

    # ============================================================
    # LINE CHART
    # ============================================================

    @staticmethod
    def line_chart(df: pd.DataFrame, x_column: str, y_column: str):

        plt.figure(figsize=(10, 6))

        plt.plot(df[x_column], df[y_column], marker="o")

        plt.title(f"{y_column} vs {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)

        plt.xticks(rotation=45)

        return VisualizationService._save_plot("line_chart.png")

    # ============================================================
    # SCATTER PLOT
    # ============================================================

    @staticmethod
    def scatter_plot(df: pd.DataFrame, x_column: str, y_column: str):

        plt.figure(figsize=(8, 6))

        plt.scatter(df[x_column], df[y_column])

        plt.title(f"{y_column} vs {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)

        return VisualizationService._save_plot("scatter_plot.png")

    # ============================================================
    # BOX PLOT
    # ============================================================

    @staticmethod
    def box_plot(df: pd.DataFrame, column_name: str):

        plt.figure(figsize=(7, 5))

        plt.boxplot(df[column_name].dropna(), vert=True)

        plt.title(f"Box Plot of {column_name}")
        plt.ylabel(column_name)

        return VisualizationService._save_plot("box_plot.png")

    # ============================================================
    # PIE CHART
    # ============================================================

    @staticmethod
    def pie_chart(df: pd.DataFrame, column_name: str):

        counts = df[column_name].value_counts()

        plt.figure(figsize=(8, 8))

        plt.pie(
            counts.values,
            labels=counts.index.astype(str),
            autopct="%1.1f%%",
            startangle=90,
        )

        plt.title(f"Pie Chart of {column_name}")

        return VisualizationService._save_plot("pie_chart.png")

    # ============================================================
    # CORRELATION HEATMAP
    # ============================================================

    @staticmethod
    def correlation_heatmap(df: pd.DataFrame):

        numeric_df = df.select_dtypes(include="number")

        plt.figure(figsize=(10, 8))

        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", linewidths=0.5)

        plt.title("Correlation Heatmap")

        return VisualizationService._save_plot("heatmap.png")
