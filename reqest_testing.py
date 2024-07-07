import requests

url = "http://127.0.0.1:8000/carts/"
headers = {
    "Authorization": "Token your_token_here",
    "Content-Type": "application/json",
}

data = {
    'telegram_id': '12343124',
    "items": [
        {"product": "product_id_1", "quantity": 2},
        {"product": "product_id_2", "quantity": 1},
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())

