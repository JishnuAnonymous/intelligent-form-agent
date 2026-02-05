import requests
import os

# Create a dummy image file
with open('test_form.txt', 'w') as f:
    f.write("This is a test form.")

url = 'http://127.0.0.1:5001/upload'
files = {'file': ('test_form.txt', open('test_form.txt', 'rb'))}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
