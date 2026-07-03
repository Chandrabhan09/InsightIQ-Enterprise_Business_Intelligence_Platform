import statistics
import json
import os
import pandas as pd


class ProfileService:

    @staticmethod
    def load_dataframe(filepath):

        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)

        elif filepath.endswith(".xlsx"):
            df = pd.read_excel(filepath)

        else:
            raise ValueError("Unsupported file type")

        return df

    @staticmethod
    def dataset_summary(df):

        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": list(df.columns),
            "missing_values": int(df.isnull().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
        }

    @staticmethod
    def missing_value_analysis(df):
        """
        Analyze missing values in the dataset.
        """

        total_missing = int(df.isnull().sum().sum())

        column_wise_missing = df.isnull().sum().to_dict()

        missing_percentage = ((df.isnull().sum() / len(df)) * 100).round(2).to_dict()

        return {
            "total_missing_values": total_missing,
            "column_wise_missing": column_wise_missing,
            "missing_percentage": missing_percentage,
        }

    @staticmethod
    def statistical_summary(df):
        """
        Generate statistical summary for numeric columns.
        """

        statistics = df.describe(include="number").round(2).to_dict()

        return statistics

    @staticmethod
    def missing_value_analysis(df):
        """
        Analyze missing values in the dataset.
        """

        total_missing = int(df.isnull().sum().sum())

        column_wise_missing = df.isnull().sum().to_dict()

        missing_percentage = ((df.isnull().sum() / len(df)) * 100).round(2).to_dict()

        return {
            "total_missing_values": total_missing,
            "column_wise_missing": column_wise_missing,
            "missing_percentage": missing_percentage,
        }

    @staticmethod
    def duplicate_analysis(df):
        """
        Analyze duplicate records in the dataset.
        """

        total_rows = len(df)

        duplicate_rows = int(df.duplicated().sum())

        duplicate_percentage = round((duplicate_rows / total_rows) * 100, 2)

        dataset_status = "Duplicates Found" if duplicate_rows > 0 else "Clean Dataset"

        return {
            "total_rows": total_rows,
            "duplicate_rows": duplicate_rows,
            "duplicate_percentage": duplicate_percentage,
            "dataset_status": dataset_status,
        }

    @staticmethod
    def data_type_analysis(df):
        """
        Analyze data types of the dataset.
        """

        data_types = {}

        for column in df.columns:
            data_types[column] = str(df[column].dtype)

        numeric_columns = len(df.select_dtypes(include="number").columns)

        categorical_columns = len(df.select_dtypes(include="object").columns)

        boolean_columns = len(df.select_dtypes(include="bool").columns)

        datetime_columns = len(df.select_dtypes(include="datetime").columns)

        return {
            "total_columns": len(df.columns),
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "boolean_columns": boolean_columns,
            "datetime_columns": datetime_columns,
            "column_data_types": data_types,
        }

    @staticmethod
    def correlation_analysis(df):
        """
        Generate correlation matrix for numeric columns.
        """

        numeric_df = df.select_dtypes(include="number")

        correlation_matrix = numeric_df.corr().round(2).to_dict()

        return {"correlation_matrix": correlation_matrix}

    @staticmethod
    def outlier_analysis(df):
        """
        Detect outliers using the IQR method.
        """

        numeric_df = df.select_dtypes(include="number")

        outlier_summary = {}

        for column in numeric_df.columns:

            Q1 = numeric_df[column].quantile(0.25)

            Q3 = numeric_df[column].quantile(0.75)

            IQR = Q3 - Q1

            lower_limit = Q1 - (1.5 * IQR)

            upper_limit = Q3 + (1.5 * IQR)

            outliers = numeric_df[
                (numeric_df[column] < lower_limit) | (numeric_df[column] > upper_limit)
            ]

            outlier_summary[column] = len(outliers)

        return {"outlier_summary": outlier_summary}

    @staticmethod
    def business_insights(df):
        """
        Generate business insights from dataset.
        """

        insights = []

        # Dataset Size
        insights.append(
            f"Dataset contains {len(df)} rows and {len(df.columns)} columns."
        )

        # Missing Values
        total_missing = int(df.isnull().sum().sum())

        if total_missing == 0:
            insights.append("No missing values detected.")
        else:
            insights.append(f"{total_missing} missing values detected.")

        # Duplicate Rows
        duplicate_rows = int(df.duplicated().sum())

        if duplicate_rows == 0:
            insights.append("No duplicate rows found.")
        else:
            insights.append(f"{duplicate_rows} duplicate rows found.")

        # Numeric Columns
        numeric_df = df.select_dtypes(include="number")

        insights.append(f"{len(numeric_df.columns)} numeric columns detected.")

        # Highest Average Column
        means = numeric_df.mean(numeric_only=True)

        highest_column = means.idxmax()

        highest_value = round(means.max(), 2)

        insights.append(
            f"{highest_column} has the highest average value ({highest_value})."
        )

        return {"business_insights": insights}

    @staticmethod
    def export_report(df):
        """
        Export complete enterprise profiling report.
        """

        os.makedirs("reports", exist_ok=True)

        report = {
            "dataset_summary": {"rows": len(df), "columns": len(df.columns)},
            "statistical_summary": ProfileService.statistical_summary(df),
            "missing_value_analysis": ProfileService.missing_value_analysis(df),
            "duplicate_analysis": ProfileService.duplicate_analysis(df),
            "data_type_analysis": ProfileService.data_type_analysis(df),
            "correlation_analysis": ProfileService.correlation_analysis(df),
            "outlier_analysis": ProfileService.outlier_analysis(df),
            "business_insights": ProfileService.business_insights(df),
        }

        report_path = "reports/profile_report.json"

        with open(report_path, "w") as file:
            json.dump(report, file, indent=4)

        return {
            "message": "Enterprise report generated successfully.",
            "report_path": report_path,
        }
