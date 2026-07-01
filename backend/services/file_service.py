import os
import shutil
from datetime import datetime

import pandas as pd

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class FileService:

    @staticmethod
    def save_file(file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"{timestamp}_{file.filename}"

        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        metadata = FileService.extract_metadata(filepath)

        return {
            "filename": filename,
            "filepath": filepath,
            "metadata": metadata
        }

    @staticmethod
    def extract_metadata(filepath):

        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)

        elif filepath.endswith(".xlsx"):
            df = pd.read_excel(filepath)

        else:
            raise ValueError("Unsupported file format")

        metadata = {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),
            "data_types": {
                column: str(dtype)
                for column, dtype in df.dtypes.items()
            },
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_usage_kb": round(
                df.memory_usage(deep=True).sum() / 1024,
                2
            ),
            "file_size_mb": round(
                os.path.getsize(filepath) / (1024 * 1024),
                2
            )
        }

        return metadata