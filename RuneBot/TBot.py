
import requests

response = requests.get("https://alexnormand-dino-ipsum.p.rapidapi.com/?format=text&words=10&paragraphs=1")

print(response.status_code)

