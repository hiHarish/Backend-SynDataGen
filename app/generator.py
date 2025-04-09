# backend/app/generator.py

from typing import List, Dict, Any
from app.schema_mapper import infer_field_type
from app.advance_mapper import get_generator

def generate_dataset(columns: List[Dict[str, str]], row_count: int) -> List[Dict[str, Any]]:
    """
    Generates synthetic dataset using selected, custom, or inferred generators.
    """
    generators = {}

    for col in columns:
        name = col["name"]
        field_type = col.get("type", "").strip().lower()
        custom_code = col.get("custom")

        # Step 1: Custom logic
        if field_type == "custom" and custom_code:
            generators[name] = get_generator("custom", custom_code)

        else:
            # Step 2: Try advanced mapper
            gen = get_generator(field_type, None, name)
            
            # Step 3: Fallback to schema_mapper (auto-infer from name)
            if hasattr(gen, "_is_fallback"):  # 🧠 This is the key change
                gen = infer_field_type(name.lower())
            generators[name] = gen

    # 🧪 Generate dataset
    return [
        {col: generators[col]() for col in generators}
        for _ in range(row_count)
    ]
