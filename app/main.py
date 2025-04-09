# backend/app/main.py

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.parser import parse_file
from app.generator import generate_dataset
from app.utils import save_as_csv, save_as_json
from app import mapper
from app import faker_types
import io
import json

# Initialize FastAPI
app = FastAPI(title="Synthetic Dataset Generator")

# Enable CORS for all origins (frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 🔗 Include router from app/mapper.py
app.include_router(faker_types.router)
app.include_router(mapper.router)

# 📤 Upload endpoint
@app.post("/upload/")
async def upload_schema(file: UploadFile = File(...)):
    """
    Accepts a schema file (.csv, .json, .xlsx) and returns extracted column headers.
    """
    try:
        columns = await parse_file(file)
        return {"columns": columns}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

# 🧪 Generate synthetic data
@app.post("/generate/")
async def generate(
    columns: str = Form(...),
    row_count: int = Form(1000),
    file_format: str = Form("csv")
):
    """
    Generates synthetic dataset from schema headers.
    """
    parsed = json.loads(columns)
    fields = parsed["fields"] if isinstance(parsed, dict) and "fields" in parsed else parsed
  # Expects a JSON string
    data = generate_dataset(fields, row_count)

    if file_format == "csv":
        csv_data = save_as_csv(data)
        return StreamingResponse(
            io.BytesIO(csv_data),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=data.csv"}
        )
    else:
        json_data = save_as_json(data)
        return StreamingResponse(
            io.BytesIO(json_data),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=data.json"}
        )
