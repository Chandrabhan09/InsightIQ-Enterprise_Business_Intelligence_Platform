import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import numpy as np
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_regression
from sklearn.model_selection import train_test_split


class PreprocessingService:
    """
    Enterprise Data Preprocessing Service
    """

    @staticmethod
    def home():
        """
        Base endpoint for preprocessing module.
        """

        return {
            "module": "Data Preprocessing & Feature Engineering",
            "status": "Active",
            "version": "1.0.0",
            "message": "Welcome to the Data Preprocessing API.",
        }

    @staticmethod
    def health():
        """
        Health check endpoint.
        """

        return {"status": "Healthy", "service": "Preprocessing Service", "ready": True}

    @staticmethod
    def handle_missing_values(df, strategy="mean"):
        """
        Handle missing values using different strategies.
        """

        missing_before = df.isnull().sum().to_dict()

        processed_df = df.copy()

        if strategy == "mean":

            numerical_columns = processed_df.select_dtypes(include=["number"]).columns

            for column in numerical_columns:

                processed_df[column] = processed_df[column].fillna(
                    processed_df[column].mean()
                )

        elif strategy == "median":

            numerical_columns = processed_df.select_dtypes(include=["number"]).columns

            for column in numerical_columns:

                processed_df[column] = processed_df[column].fillna(
                    processed_df[column].median()
                )

        elif strategy == "mode":

            for column in processed_df.columns:

                mode = processed_df[column].mode()

                if not mode.empty:

                    processed_df[column] = processed_df[column].fillna(mode.iloc[0])

        elif strategy == "drop_rows":

            processed_df = processed_df.dropna()

        elif strategy == "drop_columns":

            processed_df = processed_df.dropna(axis=1)

        else:

            raise ValueError("Invalid strategy.")

        missing_after = processed_df.isnull().sum().to_dict()

        return {
            "strategy": strategy,
            "rows_before": len(df),
            "rows_after": len(processed_df),
            "columns_before": len(df.columns),
            "columns_after": len(processed_df.columns),
            "missing_before": missing_before,
            "missing_after": missing_after,
            "processed_data": processed_df.to_dict(orient="records"),
        }

    @staticmethod
    def remove_duplicates(df):
        """
        Detect and remove duplicate rows.
        """

        duplicate_count = int(df.duplicated().sum())

        rows_before = len(df)

        processed_df = df.drop_duplicates()

        rows_after = len(processed_df)

        rows_removed = rows_before - rows_after

        return {
            "rows_before": rows_before,
            "rows_after": rows_after,
            "duplicate_rows_found": duplicate_count,
            "rows_removed": rows_removed,
            "processed_data": processed_df.to_dict(orient="records"),
        }

    @staticmethod
    def treat_outliers(df):
        """
        Detect and remove outliers using the IQR method.
        """

        processed_df = df.copy()

        numerical_columns = processed_df.select_dtypes(include=["number"]).columns

        rows_before = len(processed_df)

        outlier_summary = {}

        for column in numerical_columns:

            Q1 = processed_df[column].quantile(0.25)
            Q3 = processed_df[column].quantile(0.75)

            IQR = Q3 - Q1

            lower_bound = Q1 - (1.5 * IQR)
            upper_bound = Q3 + (1.5 * IQR)

            outlier_count = (
                (processed_df[column] < lower_bound)
                | (processed_df[column] > upper_bound)
            ).sum()

            outlier_summary[column] = {
                "lower_bound": round(float(lower_bound), 2),
                "upper_bound": round(float(upper_bound), 2),
                "outliers_detected": int(outlier_count),
            }

            processed_df = processed_df[
                (processed_df[column] >= lower_bound)
                & (processed_df[column] <= upper_bound)
            ]

        rows_after = len(processed_df)

        return {
            "rows_before": rows_before,
            "rows_after": rows_after,
            "rows_removed": rows_before - rows_after,
            "outlier_summary": outlier_summary,
            "processed_data": processed_df.to_dict(orient="records"),
        }

    @staticmethod
    def encode_categorical(df, strategy="label"):
        """
        Encode categorical columns.
        """

        processed_df = df.copy()

        categorical_columns = processed_df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        if len(categorical_columns) == 0:

            raise ValueError("No categorical columns found.")

        if strategy == "label":

            encoder = LabelEncoder()

            for column in categorical_columns:

                processed_df[column] = encoder.fit_transform(
                    processed_df[column].astype(str)
                )

        elif strategy == "onehot":

            processed_df = pd.get_dummies(
                processed_df, columns=categorical_columns, drop_first=False
            )

        elif strategy == "ordinal":

            encoder = LabelEncoder()

            for column in categorical_columns:

                processed_df[column] = encoder.fit_transform(
                    processed_df[column].astype(str)
                )

        else:

            raise ValueError("Invalid encoding strategy.")

        return {
            "encoding_strategy": strategy,
            "categorical_columns": categorical_columns,
            "columns_before": len(df.columns),
            "columns_after": len(processed_df.columns),
            "processed_data": processed_df.to_dict(orient="records"),
        }

    @staticmethod
    def scale_features(df, strategy="standard"):
        """
        Scale numerical features.
        """

        processed_df = df.copy()

        numerical_columns = processed_df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        if len(numerical_columns) == 0:

            raise ValueError("No numerical columns found.")

        if strategy == "standard":

            scaler = StandardScaler()

        elif strategy == "minmax":

            scaler = MinMaxScaler()

        elif strategy == "robust":

            scaler = RobustScaler()

        else:

            raise ValueError("Invalid scaling strategy.")

        processed_df[numerical_columns] = scaler.fit_transform(
            processed_df[numerical_columns]
        )

        return {
            "scaling_strategy": strategy,
            "scaled_columns": numerical_columns,
            "rows_processed": len(processed_df),
            "processed_data": processed_df.to_dict(orient="records"),
        }

    @staticmethod
    def feature_engineering(df):
        """
        Automatically create engineered features.
        """

        processed_df = df.copy()

        numerical_columns = processed_df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        if len(numerical_columns) < 2:
            raise ValueError("At least two numerical columns are required.")

        engineered_features = []

        # -------------------------------
        # First Two Numerical Columns
        # -------------------------------

        col1 = numerical_columns[0]
        col2 = numerical_columns[1]

        # Ratio Feature
        processed_df[f"{col1}_{col2}_ratio"] = processed_df[col1] / (
            processed_df[col2] + 1
        )

        engineered_features.append(f"{col1}_{col2}_ratio")

        # Sum Feature
        processed_df[f"{col1}_{col2}_sum"] = processed_df[col1] + processed_df[col2]

        engineered_features.append(f"{col1}_{col2}_sum")

        # Difference Feature
        processed_df[f"{col1}_{col2}_difference"] = (
            processed_df[col1] - processed_df[col2]
        )

        engineered_features.append(f"{col1}_{col2}_difference")

        # Product Feature
        processed_df[f"{col1}_{col2}_product"] = processed_df[col1] * processed_df[col2]

        engineered_features.append(f"{col1}_{col2}_product")

        # -------------------------------
        # Log & Square Root Transformations
        # -------------------------------

        for column in numerical_columns:

            if (processed_df[column] >= 0).all():

                processed_df[f"{column}_log"] = np.log1p(processed_df[column])

                processed_df[f"{column}_sqrt"] = np.sqrt(processed_df[column])

                engineered_features.extend([f"{column}_log", f"{column}_sqrt"])

        return {
            "original_columns": len(df.columns),
            "new_columns": len(processed_df.columns),
            "engineered_features": engineered_features,
            "processed_data": processed_df.to_dict(orient="records"),
        }

    @staticmethod
    def feature_selection(df, target_column, k=5):
        """
        Select important numerical features.
        """

        processed_df = df.copy()

        if target_column not in processed_df.columns:
            raise ValueError("Target column not found.")

        # Keep only numeric columns
        numeric_df = processed_df.select_dtypes(include=["number"])

        if target_column not in numeric_df.columns:
            raise ValueError("Target column must be numerical.")

        X = numeric_df.drop(columns=[target_column])
        y = numeric_df[target_column]

        if X.empty:
            raise ValueError("No numerical features available.")

        # ----------------------------
        # Variance Threshold
        # ----------------------------

        variance_selector = VarianceThreshold()

        variance_selector.fit(X)

        variance_features = X.columns[variance_selector.get_support()].tolist()

        X_variance = X[variance_features]

        # ----------------------------
        # Select K Best
        # ----------------------------

        k = min(k, X_variance.shape[1])

        selector = SelectKBest(score_func=f_regression, k=k)

        selector.fit(X_variance, y)

        selected_features = X_variance.columns[selector.get_support()].tolist()

        selected_df = processed_df[selected_features + [target_column]]

        return {
            "target_column": target_column,
            "total_features_before": len(X.columns),
            "features_after_variance_filter": len(variance_features),
            "selected_features": selected_features,
            "processed_data": selected_df.to_dict(orient="records"),
        }

    @staticmethod
    def split_dataset(df, target_column, test_size=0.2, random_state=42):
        """
        Split dataset into training and testing sets.
        """

        if target_column not in df.columns:

            raise ValueError("Target column not found.")

        X = df.drop(columns=[target_column])

        y = df[target_column]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        train_df = X_train.copy()

        train_df[target_column] = y_train

        test_df = X_test.copy()

        test_df[target_column] = y_test

        return {
            "target_column": target_column,
            "total_rows": len(df),
            "training_rows": len(train_df),
            "testing_rows": len(test_df),
            "test_size": test_size,
            "random_state": random_state,
            "training_data": train_df.to_dict(orient="records"),
            "testing_data": test_df.to_dict(orient="records"),
        }

    @staticmethod
    def preprocessing_pipeline(df):
        """
        Complete preprocessing pipeline.
        """

        processed_df = df.copy()

        summary = {}

        # -----------------------------------
        # Missing Value Treatment
        # -----------------------------------

        processed_df = processed_df.fillna(processed_df.mean(numeric_only=True))

        for column in processed_df.select_dtypes(
            include=["object", "category"]
        ).columns:

            processed_df[column] = processed_df[column].fillna(
                processed_df[column].mode()[0]
            )

        summary["missing_values"] = "Handled"

        # -----------------------------------
        # Duplicate Removal
        # -----------------------------------

        before_duplicates = len(processed_df)

        processed_df = processed_df.drop_duplicates()

        summary["duplicates_removed"] = before_duplicates - len(processed_df)

        # -----------------------------------
        # Outlier Removal (IQR)
        # -----------------------------------

        numeric_columns = processed_df.select_dtypes(include=["number"]).columns

        before_outliers = len(processed_df)

        for column in numeric_columns:

            Q1 = processed_df[column].quantile(0.25)
            Q3 = processed_df[column].quantile(0.75)

            IQR = Q3 - Q1

            lower = Q1 - (1.5 * IQR)
            upper = Q3 + (1.5 * IQR)

            processed_df = processed_df[
                (processed_df[column] >= lower) & (processed_df[column] <= upper)
            ]

        summary["outlier_rows_removed"] = before_outliers - len(processed_df)

        # -----------------------------------
        # Categorical Encoding
        # -----------------------------------

        categorical_columns = processed_df.select_dtypes(
            include=["object", "category"]
        ).columns

        processed_df = pd.get_dummies(
            processed_df, columns=categorical_columns, drop_first=False
        )

        summary["categorical_encoding"] = "One-Hot Encoding"

        # -----------------------------------
        # Feature Scaling
        # -----------------------------------

        scaler = StandardScaler()

        numeric_columns = processed_df.select_dtypes(include=["number"]).columns

        processed_df[numeric_columns] = scaler.fit_transform(
            processed_df[numeric_columns]
        )

        summary["feature_scaling"] = "StandardScaler"

        return {
            "rows_processed": len(processed_df),
            "columns_after_processing": len(processed_df.columns),
            "pipeline_summary": summary,
            "processed_data": processed_df.to_dict(orient="records"),
        }

    @staticmethod
    def export_processed_dataset(df):
        """
        Execute preprocessing pipeline
        and export processed dataset.
        """

        pipeline_result = PreprocessingService.preprocessing_pipeline(df)

        processed_df = pd.DataFrame(pipeline_result["processed_data"])

        export_folder = "exports"

        os.makedirs(export_folder, exist_ok=True)

        export_path = os.path.join(export_folder, "processed_dataset.csv")

        processed_df.to_csv(export_path, index=False)

        return {
            "message": "Dataset exported successfully.",
            "export_path": export_path,
            "rows_exported": len(processed_df),
            "columns_exported": len(processed_df.columns),
        }
