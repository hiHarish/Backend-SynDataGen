# backend/app/mapper.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from app.schema_mapper import infer_field_type

router = APIRouter()

class ColumnList(BaseModel):
    columns: List[str]

@router.post("/map/")
async def map_columns(payload: ColumnList) -> Dict[str, List[Dict[str, str]]]:
    mapped_fields = []
    for col in payload.columns:
        inferred = infer_field_type(col)
        field_type = getattr(inferred, "__name__", "custom")
        mapped_fields.append({
            "name": col,
            "type": field_type,
            "source": "auto"
        })
    return {"fields": mapped_fields}
