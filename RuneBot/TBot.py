
import requests

response = requests.get("https://net.runelite.api")

print(response.status_code)

print(response.json())