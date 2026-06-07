import requests
from bs4 import BeautifulSoup
import os

HEADERS = {"User-Agent": "Mozilla/5.0 (UnofficialGuide/0.1)"}

def fetch_wordpress(url, out_path):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # WordPress wraps post text in .entry-content
    content = soup.find("div", class_="entry-content")
    if content is None:
        content = soup.find("article") or soup  # fallback
    text = content.get_text(separator="\n\n", strip=True)

    # Cut everything from "Share this" onward (boilerplate)
    for marker in ["Share this:", "### Share this"]:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text.strip())
    print(f"✓ Saved {len(text)} chars to {out_path}")
    return text

fetch_wordpress(
    "https://campusobscura.wordpress.com/2024/06/13/uci-undergraduate-housing-communities-ranked-an-unfiltered-guide/",
    "data/raw/wordpress_housing_ranked.txt",
)