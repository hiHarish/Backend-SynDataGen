# backend/app/schema_mapper.py

from faker import Faker
from typing import Callable

fake = Faker()

def infer_field_type(field_type: str):
    field_type = field_type.lower()

    mapping = {
        # 👤 Personal
        "name": fake.name,
        "full_name": fake.name,
        "first_name": fake.first_name,
        "last_name": fake.last_name,
        "gender": lambda: fake.random_element(elements=["Male", "Female", "Other"]),

        # 📧 Contact
        "email": fake.email,
        "phone": fake.phone_number,
        "mobile": fake.phone_number,

        # 📅 Dates
        "dob": fake.date_of_birth,
        "birth": fake.date_of_birth,
        "date": fake.date,

        # 🏠 Address
        "address": fake.address,
        "city": fake.city,
        "state": fake.state,
        "country": fake.country,
        "zip": fake.postcode,
        "postal": fake.postcode,

        # 💼 Work
        "company": fake.company,
        "job": fake.job,
        "salary": lambda: round(fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=30000, max_value=200000), 2),
        "price": lambda: round(fake.pyfloat(left_digits=4, right_digits=2, positive=True, min_value=10, max_value=9999), 2),
        "amount": lambda: round(fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=100, max_value=50000), 2),

        # 🧾 IDs
        "id": fake.uuid4,
        "uuid": fake.uuid4,

        # 🔗 Web & Tech
        "url": fake.url,
        "website": fake.url,
        "ip": fake.ipv4,
        "mac": fake.mac_address,

        # 📊 Status / Logic
        "status": lambda: fake.random_element(elements=["Active", "Inactive", "Pending"]),
        "boolean": fake.pybool,  # ✅ FIXED
        "bool": fake.pybool,     # ✅ Also alias
        "yesno": lambda: fake.random_element(elements=["Yes", "No"]),

        # 🎨 Extras (optional, nice-to-haves)
        "color": fake.color_name,
        "hex_color": fake.hex_color,
        "country_code": fake.country_code,
        "language": fake.language_code,
    }

    if field_type not in mapping:
        print(f"[⚠️] Unknown type: {field_type}. Falling back to word.")
    
    return mapping.get(field_type, fake.word)  # safe fallback