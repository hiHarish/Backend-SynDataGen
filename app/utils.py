# backend/app/utils.py

import pandas as pd
from typing import List, Dict
import io

def save_as_csv(data: List[Dict], filename: str = "dataset.csv") -> bytes:
    """
    Converts list of dictionaries to CSV byte stream.

    Args:
        data (List[Dict]): The dataset to export.
        filename (str): Desired output filename (not used internally here).

    Returns:
        bytes: CSV file content as byte stream.
    """
    df = pd.DataFrame(data)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode('utf-8')


def save_as_json(data: List[Dict], filename: str = "dataset.json") -> bytes:
    """
    Converts list of dictionaries to JSON byte stream.

    Args:
        data (List[Dict]): The dataset to export.
        filename (str): Desired output filename (not used internally here).

    Returns:
        bytes: JSON file content as byte stream.
    """
    buffer = io.StringIO()
    pd.DataFrame(data).to_json(buffer, orient="records", indent=2)
    return buffer.getvalue().encode('utf-8')
