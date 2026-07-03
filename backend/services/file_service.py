import os
import shutil
from datetime import datetime

import pandas as pd

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class FileService:
    """
    Handles file storage and dataset metadata extraction.
    """

    @staticmethod
    def save_file(file):
        """
        Save the uploaded file and return its metadata.
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        metadata = FileService.extract_metadata(filepath)

        return {"filename": filename, "filepath": filepath, "metadata": metadata}

    @staticmethod
    def read_dataframe(filepath):
        """
        Read CSV or Excel file into a Pandas DataFrame.
        """

        if filepath.lower().endswith(".csv"):
            return pd.read_csv(filepath)

        elif filepath.lower().endswith(".xlsx"):
            return pd.read_excel(filepath)

        else:
            raise ValueError("Unsupported file format.")

    @staticmethod
    def extract_metadata(filepath):
        """
        Extract useful metadata from the uploaded dataset.
        """

        df = FileService.read_dataframe(filepath)

        metadata = {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),
            "data_types": {column: str(dtype) for column, dtype in df.dtypes.items()},
            "missing_values": {
                column: int(value) for column, value in df.isnull().sum().items()
            },
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_usage_kb": round(df.memory_usage(deep=True).sum() / 1024, 2),
            "file_size_mb": round(os.path.getsize(filepath) / (1024 * 1024), 2),
        }

        return metadata
