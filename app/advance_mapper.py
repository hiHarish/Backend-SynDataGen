from faker import Faker
import random

fake = Faker()

def fallback():
    def _fallback():
        return fake.word()
    _fallback._is_fallback = True
    return _fallback

# Custom logic generators
def custom_yes_no(): return random.choice(["Yes", "No"])
def custom_age(): return random.randint(1, 100)
def custom_percentage(): return round(random.uniform(0.0, 100.0), 2)
def custom_invoice(): return f"INV-{fake.random_number(digits=6)}"
def custom_gstin(): return f"{fake.random_number(digits=15)}GST"

ADVANCED_TYPE_MAP = {
    # 🧑 Personal
    "first_name": fake.first_name,
    "last_name": fake.last_name,
    "phone": fake.phone_number,
    "mobile": fake.phone_number,

    # 🏢 Business
    "company": fake.company,
    "job": fake.job,
    "salary": lambda: round(fake.pyfloat(left_digits=5, right_digits=2, positive=True), 2),
    "price": lambda: round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2),

    # 🌍 Address
    "address": fake.address,
    "street_address": fake.street_address,
    "street_name": fake.street_name,
    "city": fake.city,
    "state": fake.state,
    "country": fake.country,
    "postcode": fake.postcode,
    "zipcode": fake.postcode,
    "zip": fake.postcode,
    "uri": fake.uri_path,
    "domain": fake.domain_name,
    "domain_name": fake.domain_name,
    "ipv4": fake.ipv4,
    "ip": fake.ipv4,

    # 📅 Dates
    "date": fake.date,
    "dob": fake.date_of_birth,
    "birth": fake.date_of_birth,
    "id": fake.uuid4,

    "name": fake.name,
    "email": fake.email,
    "uuid4": fake.uuid4,
    "url": fake.url,
    "phone_number": fake.phone_number,
    "boolean": fake.pybool,
    "random_int": fake.random_int,
    "pyint": fake.pyint,
    "pyfloat": fake.pyfloat,
    "ipv6": fake.ipv6,
    "mac_address": fake.mac_address,
    "user_name": fake.user_name,
    "latitude": fake.latitude,
    "longitude": fake.longitude,
    "time": fake.time,
    "datetime": lambda: str(fake.date_time()),
    "date_time": lambda: str(fake.date_time()),
    "date_of_birth": lambda: str(fake.date_of_birth()),
    "century": fake.century,
    "month": fake.month_name,
    "year": fake.year,
    "day_of_week": fake.day_of_week,
    "day_of_month": fake.day_of_month,
    "timezone": fake.timezone,
    "bs": fake.bs,
    "credit_card_number": fake.credit_card_number,
    "credit_card_expire": fake.credit_card_expire,
    "credit_card_provider": fake.credit_card_provider,
    "iban": fake.iban,
    "bank_country": fake.bank_country,
    "file_name": fake.file_name,
    "file_path": fake.file_path,
    "mime_type": fake.mime_type,
    "password": fake.password,
    "language_code": fake.language_code,
    "currency_name": fake.currency_name,
    "color_name": fake.color_name,
    "emoji": fake.emoji,

    # Your custom logic preserved
    "yes_no": custom_yes_no,
    "age": custom_age,
    "percentage": custom_percentage,
    "invoice_number": custom_invoice,
    "gstin": custom_gstin,
    "text_50": lambda: fake.text(max_nb_chars=50),
    "text_100": lambda: fake.text(max_nb_chars=100),
    
    "bool": fake.pybool,
    "gender": lambda: fake.random_element(elements=["Male", "Female", "Other"]),
    "status": lambda: fake.random_element(elements=["Active", "Inactive", "Pending"]),
    "color": fake.color_name,
    "hex_color": fake.hex_color,
    "country_code": fake.country_code,
    "language": fake.language_code,
    

}

_index_counter = {}

def index_generator_for(field_name):
    def generator():
        _index_counter[field_name] = _index_counter.get(field_name, 0) + 1
        return _index_counter[field_name]
    return generator


def compile_custom_logic(code: str):
    try:
        return eval(f"lambda: {code}", {"random": random, "fake": fake})
    except Exception as e:
        print(f"[⚠️] Custom logic failed: {e}")
        return fallback

def get_generator(field_type: str, custom_code: str = None,field_name: str = ""):
    key = field_type.strip().lower()
    if key == "custom" and custom_code:
        return compile_custom_logic(custom_code)
    if key == "index.no":
        return index_generator_for(field_name)
    return ADVANCED_TYPE_MAP.get(key, fallback())
