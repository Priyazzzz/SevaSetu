import requests
from bs4 import BeautifulSoup

url = "https://www.myscheme.gov.in/schemes/pmay-u"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

text = soup.get_text(" ", strip=True)

print("\n--- PAGE TEXT PREVIEW ---\n")
print(text[:3000])