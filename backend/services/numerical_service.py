import numpy as np
import pandas as pd
from datetime import datetime
import time
import matplotlib.pyplot as plt
from pathlib import Path


class NumericalService:
    """
    Enterprise Numerical Computing Service.
    """

    @staticmethod
    def health_check():
        """
        Verify that the numerical service is working.
        """

        return {
            "service": "Numerical Computing Engine",
            "status": "Running",
            "numpy_version": np.__version__,
        }

    @staticmethod
    def numerical_summary(df, column_name):
        """
        Generate enterprise numerical summary using NumPy.
        """

        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found.")

        if not pd.api.types.is_numeric_dtype(df[column_name]):
            raise ValueError(f"Column '{column_name}' is not numeric.")

        data = df[column_name].dropna().to_numpy()

        summary = {
            "column": column_name,
            "count": int(data.size),
            "mean": round(float(np.mean(data)), 2),
            "median": round(float(np.median(data)), 2),
            "minimum": round(float(np.min(data)), 2),
            "maximum": round(float(np.max(data)), 2),
            "range": round(float(np.max(data) - np.min(data)), 2),
            "variance": round(float(np.var(data)), 2),
            "standard_deviation": round(float(np.std(data)), 2),
        }

        return summary

    @staticmethod
    def percentile_summary(df, column_name):
        """
        Generate percentile summary using NumPy.
        """

        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found.")

        if not pd.api.types.is_numeric_dtype(df[column_name]):
            raise ValueError(f"Column '{column_name}' is not numeric.")

        data = df[column_name].dropna().to_numpy()

        p10 = np.percentile(data, 10)
        q1 = np.percentile(data, 25)
        median = np.percentile(data, 50)
        q3 = np.percentile(data, 75)
        p90 = np.percentile(data, 90)

        return {
            "column": column_name,
            "10th_percentile": round(float(p10), 2),
            "25th_percentile": round(float(q1), 2),
            "50th_percentile": round(float(median), 2),
            "75th_percentile": round(float(q3), 2),
            "90th_percentile": round(float(p90), 2),
            "interquartile_range": round(float(q3 - q1), 2),
        }

    @staticmethod
    def advanced_statistics(df, column_name):
        """
        Generate advanced statistical metrics.
        """

        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found.")

        if not pd.api.types.is_numeric_dtype(df[column_name]):
            raise ValueError(f"Column '{column_name}' is not numeric.")

        data = df[column_name].dropna().to_numpy()

        mean = np.mean(data)
        std = np.std(data)

        if mean == 0:
            cv = None
        else:
            cv = (std / mean) * 100

        skewness = pd.Series(data).skew()
        kurtosis = pd.Series(data).kurt()

        return {
            "column": column_name,
            "mean": round(float(mean), 2),
            "standard_deviation": round(float(std), 2),
            "coefficient_of_variation": (None if cv is None else round(float(cv), 2)),
            "skewness": round(float(skewness), 4),
            "kurtosis": round(float(kurtosis), 4),
        }

    @staticmethod
    def normalize_data(df, column_name, method="minmax"):
        """
        Normalize numerical data.
        """

        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found.")

        if not pd.api.types.is_numeric_dtype(df[column_name]):
            raise ValueError(f"Column '{column_name}' is not numeric.")

        data = df[column_name].dropna().to_numpy(dtype=float)

        if method == "minmax":

            minimum = np.min(data)
            maximum = np.max(data)

            if maximum == minimum:
                normalized = np.zeros_like(data)

            else:
                normalized = (data - minimum) / (maximum - minimum)

        elif method == "decimal":

            max_abs = np.max(np.abs(data))

            if max_abs == 0:
                normalized = data

            else:
                digits = len(str(int(max_abs)))

                normalized = data / (10**digits)

        else:
            raise ValueError("Method must be 'minmax' or 'decimal'.")

        return {
            "column": column_name,
            "method": method,
            "total_values": int(len(normalized)),
            "normalized_values": [round(float(value), 4) for value in normalized[:20]],
        }

    @staticmethod
    def standardize_data(df, column_name):
        """
        Standardize numerical data using Z-score.
        """

        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found.")

        if not pd.api.types.is_numeric_dtype(df[column_name]):
            raise ValueError(f"Column '{column_name}' is not numeric.")

        data = df[column_name].dropna().to_numpy(dtype=float)

        mean = np.mean(data)
        std = np.std(data)

        if std == 0:
            standardized = np.zeros_like(data)
        else:
            standardized = (data - mean) / std

        return {
            "column": column_name,
            "mean": round(float(mean), 2),
            "standard_deviation": round(float(std), 2),
            "total_values": int(len(standardized)),
            "standardized_values": [
                round(float(value), 4) for value in standardized[:20]
            ],
        }

    @staticmethod
    def matrix_operations(df):
        """
        Perform enterprise matrix operations using dataset.
        """

        numeric_df = df.select_dtypes(include=["number"])

        if numeric_df.empty:
            raise ValueError("Dataset contains no numeric columns.")

        matrix = numeric_df.to_numpy()

        transpose = matrix.T

        multiplication = np.matmul(transpose, matrix)

        return {
            "matrix_shape": list(matrix.shape),
            "transpose_shape": list(transpose.shape),
            "matrix_rank": int(np.linalg.matrix_rank(matrix)),
            "multiplication_shape": list(multiplication.shape),
            "sample_matrix": matrix[:5].tolist(),
            "sample_transpose": transpose[:, :5].tolist(),
            "sample_multiplication": multiplication.tolist(),
        }

    @staticmethod
    def linear_algebra_analysis(df):
        """
        Perform enterprise linear algebra analysis.
        """

        numeric_df = df.select_dtypes(include=["number"])

        if numeric_df.empty:
            raise ValueError("Dataset contains no numeric columns.")

        matrix = numeric_df.to_numpy(dtype=float)

        # Use first 5 numeric columns only
        if matrix.shape[1] > 5:
            matrix = matrix[:, :5]

        # Create square matrix
        square_matrix = np.matmul(matrix.T, matrix)

        determinant = float(np.linalg.det(square_matrix))

        rank = int(np.linalg.matrix_rank(square_matrix))

        eigen_values, eigen_vectors = np.linalg.eig(square_matrix)

        try:
            inverse = np.linalg.inv(square_matrix)

            inverse_result = inverse.tolist()

        except np.linalg.LinAlgError:

            inverse_result = "Matrix is singular. Inverse cannot be calculated."

        return {
            "matrix_size": list(square_matrix.shape),
            "rank": rank,
            "determinant": round(determinant, 4),
            "eigen_values": [round(float(value), 4) for value in eigen_values],
            "eigen_vectors": [
                [round(float(item), 4) for item in row] for row in eigen_vectors
            ],
            "inverse": inverse_result,
        }

    @staticmethod
    def performance_benchmark(df, column_name):
        """
        Compare NumPy and Pandas performance.
        """

        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found.")

        if not pd.api.types.is_numeric_dtype(df[column_name]):
            raise ValueError(f"Column '{column_name}' is not numeric.")

        pandas_data = df[column_name].dropna()

        numpy_data = pandas_data.to_numpy()

        # ------------------------
        # Mean Benchmark
        # ------------------------

        start = time.perf_counter()
        np.mean(numpy_data)
        numpy_mean_time = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        pandas_data.mean()
        pandas_mean_time = (time.perf_counter() - start) * 1000

        # ------------------------
        # Standard Deviation Benchmark
        # ------------------------

        start = time.perf_counter()
        np.std(numpy_data)
        numpy_std_time = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        pandas_data.std()
        pandas_std_time = (time.perf_counter() - start) * 1000

        # ------------------------
        # Sum Benchmark
        # ------------------------

        start = time.perf_counter()
        np.sum(numpy_data)
        numpy_sum_time = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        pandas_data.sum()
        pandas_sum_time = (time.perf_counter() - start) * 1000

        return {
            "column": column_name,
            "numpy": {
                "mean_ms": round(numpy_mean_time, 6),
                "std_ms": round(numpy_std_time, 6),
                "sum_ms": round(numpy_sum_time, 6),
            },
            "pandas": {
                "mean_ms": round(pandas_mean_time, 6),
                "std_ms": round(pandas_std_time, 6),
                "sum_ms": round(pandas_sum_time, 6),
            },
            "overall_faster": (
                "NumPy" if numpy_mean_time < pandas_mean_time else "Pandas"
            ),
        }

    @staticmethod
    def generate_numerical_report(df, column_name):
        """
        Generate a complete enterprise numerical analytics report.
        """

        report = {
            "report_information": {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "column": column_name,
                "total_rows": int(len(df)),
            },
            "numerical_summary": NumericalService.numerical_summary(df, column_name),
            "percentile_analysis": NumericalService.percentile_summary(df, column_name),
            "advanced_statistics": NumericalService.advanced_statistics(
                df, column_name
            ),
            "normalization_preview": NumericalService.normalize_data(
                df, column_name, "minmax"
            ),
            "standardization_preview": NumericalService.standardize_data(
                df, column_name
            ),
            "performance_benchmark": NumericalService.performance_benchmark(
                df, column_name
            ),
        }

        return report

    @staticmethod
    def generate_visualizations(df, column_name):
        """
        Generate numerical visualization charts.
        """

        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found.")

        if not pd.api.types.is_numeric_dtype(df[column_name]):
            raise ValueError(f"Column '{column_name}' is not numeric.")

        data = df[column_name].dropna()

        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)

        # ---------------- Histogram ----------------
        plt.figure(figsize=(8, 5))
        plt.hist(data, bins=30)
        plt.title(f"{column_name} Histogram")
        plt.xlabel(column_name)
        plt.ylabel("Frequency")
        histogram_path = output_dir / f"{column_name}_histogram.png"
        plt.tight_layout()
        plt.savefig(histogram_path)
        plt.close()

        # ---------------- Box Plot ----------------
        plt.figure(figsize=(6, 5))
        plt.boxplot(data)
        plt.title(f"{column_name} Box Plot")
        boxplot_path = output_dir / f"{column_name}_boxplot.png"
        plt.tight_layout()
        plt.savefig(boxplot_path)
        plt.close()

        # ---------------- Line Chart ----------------
        plt.figure(figsize=(10, 5))
        plt.plot(data.values)
        plt.title(f"{column_name} Line Chart")
        plt.xlabel("Row Index")
        plt.ylabel(column_name)
        linechart_path = output_dir / f"{column_name}_linechart.png"
        plt.tight_layout()
        plt.savefig(linechart_path)
        plt.close()

        return {
            "message": "Visualization report generated successfully.",
            "histogram": str(histogram_path),
            "boxplot": str(boxplot_path),
            "linechart": str(linechart_path),
        }
