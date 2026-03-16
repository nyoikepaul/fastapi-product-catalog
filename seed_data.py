import requests

# Your LIVE production URL
API_URL = "https://fastapi-product-catalog.vercel.app/products/"

products = [
    {"name": "Logitech MX Master 3S", "description": "High-performance wireless ergonomic mouse with 8K DPI.", "price": 99.99},
    {"name": "Keychron K2 V2", "description": "Tactile wireless mechanical keyboard with RGB backlighting.", "price": 79.99},
    {"name": "Dell UltraSharp 27", "description": "4K USB-C Hub Monitor with 100% sRGB color coverage.", "price": 549.00},
    {"name": "Sony WH-1000XM5", "description": "Industry-leading noise-canceling wireless headphones.", "price": 398.00},
    {"name": "MacBook Air M3", "description": "13-inch laptop with Apple M3 chip and 18-hour battery life.", "price": 1099.00}
]

def seed():
    print(f"🚀 Seeding data to {API_URL}...")
    for p in products:
        response = requests.post(API_URL, json=p)
        if response.status_code == 200:
            print(f"✅ Added: {p['name']}")
        else:
            print(f"❌ Failed {p['name']}: {response.text}")

if __name__ == "__main__":
    seed()
