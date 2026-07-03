import pandas as pd
import json
import os
from datetime import datetime


class EDAService:
    """
    Enterprise Exploratory Data Analysis Service
    """

    @staticmethod
    def health_check():
        return {
            "module": "Exploratory Data Analysis",
            "status": "Running",
            "version": "1.0.0",
        }

    @staticmethod
    def dataset_overview(df):
        """
        Generate enterprise dataset overview.
        """

        numerical_columns = df.select_dtypes(include=["number"]).columns.tolist()

        categorical_columns = df.select_dtypes(exclude=["number"]).columns.tolist()

        overview = {
            "dataset_information": {
                "total_rows": int(df.shape[0]),
                "total_columns": int(df.shape[1]),
                "shape": list(df.shape),
                "memory_usage_mb": round(
                    df.memory_usage(deep=True).sum() / 1024 / 1024, 2
                ),
            },
            "quality_summary": {
                "total_missing_values": int(df.isnull().sum().sum()),
                "duplicate_rows": int(df.duplicated().sum()),
            },
            "columns": {
                "column_names": df.columns.tolist(),
                "data_types": {
                    column: str(dtype) for column, dtype in df.dtypes.items()
                },
                "numerical_columns": numerical_columns,
                "categorical_columns": categorical_columns,
            },
        }

        return overview

    @staticmethod
    def missing_value_analysis(df):
        """
        Perform enterprise missing value analysis.
        """

        total_rows = len(df)

        missing_count = df.isnull().sum()

        missing_percentage = ((missing_count / total_rows) * 100).round(2)

        missing_df = missing_percentage[missing_percentage > 0].sort_values(
            ascending=False
        )

        quality_score = round(
            (1 - (missing_count.sum() / (df.shape[0] * df.shape[1]))) * 100, 2
        )

        return {
            "summary": {
                "total_missing_values": int(missing_count.sum()),
                "columns_with_missing_values": int((missing_count > 0).sum()),
                "data_quality_score": quality_score,
            },
            "missing_values": {
                column: int(count) for column, count in missing_count.items()
            },
            "missing_percentage": {
                column: float(percent) for column, percent in missing_percentage.items()
            },
            "missing_ranking": missing_df.to_dict(),
        }

    @staticmethod
    def duplicate_analysis(df):
        """
        Perform enterprise duplicate analysis.
        """

        total_rows = len(df)

        duplicate_rows = df.duplicated().sum()

        duplicate_percentage = round((duplicate_rows / total_rows) * 100, 2)

        unique_rows = total_rows - duplicate_rows

        uniqueness_score = round((unique_rows / total_rows) * 100, 2)

        duplicate_samples = df[df.duplicated()].head(5)

        return {
            "summary": {
                "total_rows": total_rows,
                "duplicate_rows": int(duplicate_rows),
                "unique_rows": int(unique_rows),
                "duplicate_percentage": duplicate_percentage,
                "uniqueness_score": uniqueness_score,
            },
            "duplicate_status": (
                "Excellent" if duplicate_percentage == 0 else "Duplicates Found"
            ),
            "sample_duplicates": duplicate_samples.to_dict(orient="records"),
        }

    @staticmethod
    def column_classification(df):
        """
        Classify dataset columns into business-friendly categories.
        """

        report = {}

        for column in df.columns:

            dtype = str(df[column].dtype)

            unique_values = int(df[column].nunique())

            total_values = int(len(df))

            if pd.api.types.is_numeric_dtype(df[column]):
                category = "Numerical"

            elif pd.api.types.is_bool_dtype(df[column]):
                category = "Boolean"

            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                category = "DateTime"

            else:

                average_length = df[column].astype(str).str.len().mean()

                if average_length > 25:
                    category = "Text"
                else:
                    category = "Categorical"

            cardinality = "High" if unique_values > total_values * 0.20 else "Low"

            report[column] = {
                "data_type": dtype,
                "classification": category,
                "unique_values": unique_values,
                "missing_values": int(df[column].isnull().sum()),
                "cardinality": cardinality,
            }

        return report

    @staticmethod
    def distribution_analysis(df):
        """
        Analyze numerical column distributions.
        """

        numerical_columns = df.select_dtypes(include=["number"])

        if numerical_columns.empty:
            raise ValueError("Dataset contains no numerical columns.")

        report = {}

        for column in numerical_columns.columns:

            data = numerical_columns[column].dropna()

            skewness = data.skew()

            kurtosis = data.kurt()

            if abs(skewness) < 0.5:
                distribution = "Approximately Normal"

            elif skewness > 0.5:
                distribution = "Right Skewed"

            else:
                distribution = "Left Skewed"

            report[column] = {
                "count": int(data.count()),
                "mean": round(float(data.mean()), 2),
                "median": round(float(data.median()), 2),
                "std": round(float(data.std()), 2),
                "minimum": round(float(data.min()), 2),
                "maximum": round(float(data.max()), 2),
                "skewness": round(float(skewness), 4),
                "kurtosis": round(float(kurtosis), 4),
                "distribution": distribution,
            }

        return report

    @staticmethod
    def categorical_analysis(df):
        """
        Analyze categorical columns.
        """

        categorical_columns = df.select_dtypes(exclude=["number"])

        if categorical_columns.empty:
            raise ValueError("Dataset contains no categorical columns.")

        report = {}

        for column in categorical_columns.columns:

            data = categorical_columns[column].fillna("Missing")

            value_counts = data.value_counts()

            total = len(data)

            top_categories = {}

            for category, count in value_counts.head(10).items():

                top_categories[str(category)] = {
                    "count": int(count),
                    "percentage": round((count / total) * 100, 2),
                }

            report[column] = {
                "unique_values": int(data.nunique()),
                "mode": str(value_counts.index[0]),
                "mode_frequency": int(value_counts.iloc[0]),
                "cardinality": ("High" if data.nunique() > total * 0.20 else "Low"),
                "top_categories": top_categories,
            }

        return report

    @staticmethod
    def correlation_analysis(df):
        """
        Analyze correlations between numerical columns.
        """

        numerical_df = df.select_dtypes(include=["number"])

        if numerical_df.shape[1] < 2:
            raise ValueError("At least two numerical columns are required.")

        correlation_matrix = numerical_df.corr()

        strong_positive = []

        strong_negative = []

        weak = []

        columns = correlation_matrix.columns

        for i in range(len(columns)):

            for j in range(i + 1, len(columns)):

                value = correlation_matrix.iloc[i, j]

                pair = {
                    "feature_1": columns[i],
                    "feature_2": columns[j],
                    "correlation": round(float(value), 4),
                }

                if value >= 0.70:
                    strong_positive.append(pair)

                elif value <= -0.70:
                    strong_negative.append(pair)

                elif abs(value) < 0.30:
                    weak.append(pair)

        return {
            "correlation_matrix": correlation_matrix.round(4).to_dict(),
            "summary": {
                "strong_positive": strong_positive,
                "strong_negative": strong_negative,
                "weak_correlations": weak,
            },
        }

    @staticmethod
    def outlier_analysis(df):
        """
        Detect outliers using the IQR method.
        """

        numerical_df = df.select_dtypes(include=["number"])

        if numerical_df.empty:
            raise ValueError("Dataset contains no numerical columns.")

        report = {}

        for column in numerical_df.columns:

            data = numerical_df[column].dropna()

            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            outliers = data[(data < lower_bound) | (data > upper_bound)]

            report[column] = {
                "q1": round(float(q1), 2),
                "q3": round(float(q3), 2),
                "iqr": round(float(iqr), 2),
                "lower_bound": round(float(lower_bound), 2),
                "upper_bound": round(float(upper_bound), 2),
                "outlier_count": int(len(outliers)),
                "outlier_percentage": round((len(outliers) / len(data)) * 100, 2),
                "sample_outliers": [
                    round(float(value), 2) for value in outliers.head(10)
                ],
            }

        return report

    @staticmethod
    def business_insights(df):
        """
        Generate automated business insights.
        """

        insights = []

        rows, columns = df.shape

        insights.append(f"The dataset contains {rows} rows and {columns} columns.")

        total_missing = int(df.isnull().sum().sum())

        if total_missing == 0:
            insights.append("Excellent data quality. No missing values were detected.")
        else:
            insights.append(
                f"The dataset contains {total_missing} missing values. Data cleaning is recommended."
            )

        duplicate_rows = int(df.duplicated().sum())

        if duplicate_rows == 0:
            insights.append("No duplicate records were found.")
        else:
            insights.append(
                f"{duplicate_rows} duplicate rows were detected. Consider removing them before modeling."
            )

        numerical_columns = df.select_dtypes(include=["number"]).columns.tolist()

        categorical_columns = df.select_dtypes(exclude=["number"]).columns.tolist()

        insights.append(
            f"The dataset contains {len(numerical_columns)} numerical features."
        )

        insights.append(
            f"The dataset contains {len(categorical_columns)} categorical features."
        )

        if len(numerical_columns) >= 5:
            insights.append(
                "The dataset is well suited for statistical analysis and machine learning."
            )

        if len(categorical_columns) > 0:
            insights.append(
                "Categorical features can be encoded for predictive modeling."
            )

        recommendations = []

        if total_missing > 0:
            recommendations.append(
                "Handle missing values before training machine learning models."
            )

        if duplicate_rows > 0:
            recommendations.append("Remove duplicate records to improve data quality.")

        recommendations.append("Perform feature engineering before model training.")

        recommendations.append(
            "Normalize or standardize numerical features when required."
        )

        return {"business_insights": insights, "recommendations": recommendations}

    @staticmethod
    def export_report(df):
        """
        Export complete EDA report to a JSON file.
        """

        export_folder = "exports"

        os.makedirs(export_folder, exist_ok=True)

        report = {
            "overview": EDAService.dataset_overview(df),
            "missing_analysis": EDAService.missing_value_analysis(df),
            "duplicate_analysis": EDAService.duplicate_analysis(df),
            "column_classification": EDAService.column_classification(df),
            "distribution_analysis": EDAService.distribution_analysis(df),
            "categorical_analysis": EDAService.categorical_analysis(df),
            "correlation_analysis": EDAService.correlation_analysis(df),
            "outlier_analysis": EDAService.outlier_analysis(df),
            "business_insights": EDAService.business_insights(df),
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_file = os.path.join(export_folder, f"eda_report_{timestamp}.json")

        with open(output_file, "w", encoding="utf-8") as file:

            json.dump(report, file, indent=4)

        return {
            "status": "Success",
            "message": "EDA report exported successfully.",
            "report_path": output_file,
        }
