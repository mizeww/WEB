from requests import get, post, delete, put
URL = "http://127.0.0.1:8081"

print(get(f"{URL}/api/news/1").json())