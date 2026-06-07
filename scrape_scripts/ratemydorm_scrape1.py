import requests
from bs4 import BeautifulSoup
import os

HEADERS = {"User-Agent": "Mozilla/5.0 (UnofficialGuide/0.1)"}

def fetch_ratemydorm(url, out_path):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n", strip=True)

    # Reviews live between these two markers on the page
    start = text.find("Student Reviews")
    end = text.find("Browse dorms on campus")
    if start != -1 and end != -1:
        text = text[start:end]

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text.strip())
    print(f"✓ Saved {len(text)} chars to {out_path}")
    return text

fetch_ratemydorm(
    "https://www.ratemydorm.com/dorms-ranked/university-of-california-irvine",
    "data/raw/ratemydorm_ranked.txt",
)