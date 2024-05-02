import requests

url = 'http://127.0.0.1:8000/categories/'

response = requests.get(url).json()
# print(response)  # Print the JSON response
print(response[0])
