import os
import requests

URL = "http://localhost:8000/download/"

data = {
    "url": "https://www.youtube.com/watch?v=0mAgrrIaJCE"
}

response = requests.post(URL, json=data)
print(response)