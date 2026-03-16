import requests, os
from dotenv import load_dotenv
load_dotenv(".env.local")
API_URL = "https://secure-catalog-api.vercel.app/products/"
headers = {"X-API-Key": os.getenv("CATALOG_API_KEY"), "Content-Type": "application/json"}
products = [
    {"name": "Logitech MX Master 3S", "description": "High-performance mouse", "price": 99.99},
    {"name": "Keychron K2 V2", "description": "Mechanical keyboard", "price": 79.99}
]
for p in products:
    r = requests.post(API_URL, json=p, headers=headers)
    print(f"{'✅' if r.status_code < 300 else '❌'} {p['name']}: {r.status_code}")
