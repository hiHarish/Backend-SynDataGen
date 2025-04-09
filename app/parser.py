from typing import List
from fastapi import UploadFile
import pandas as pd
import io

SUPPORTED_FORMATS = ['csv', 'json', 'xlsx']

async def parse_file(file: UploadFile) -> List[str]:
    """
    Parses an uploaded file (.csv, .json, .xlsx) to extract column headers (schema).
    """
    filename = file.filename.lower()
    ext = filename.split('.')[-1]

    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported file format: {ext}")

    try:
        content = await await_file_read(file)  # ✅ Awaiting async function

        if ext == 'csv':
            df = pd.read_csv(io.BytesIO(content), nrows=1)
        elif ext == 'json':
            df = pd.read_json(io.BytesIO(content), orient='records', typ='frame')
        elif ext == 'xlsx':
            df = pd.read_excel(io.BytesIO(content), engine='openpyxl', nrows=1)
        else:
            raise ValueError("Unsupported file type")

        columns = df.columns.tolist()
        if not columns:
            raise ValueError("No columns found in schema")
        return columns

    except Exception as e:
        raise ValueError(f"Failed to parse file: {str(e)}")


async def await_file_read(file: UploadFile) -> bytes:
    """
    Async wrapper for file.read() with seek reset.
    """
    content = await file.read()
    file.file.seek(0)
    return content
