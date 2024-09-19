import os
import requests

URL = f"http://localhost:8000/generate/0mAgrrIaJCE?dest=en" # en, ja, ko, zh
response = requests.post(URL)