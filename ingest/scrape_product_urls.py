# ingest/scrape_product_urls.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import os

BASE_URL = "https://www.developer.tech.gov.sg"
INDEX_URL = f"{BASE_URL}/products/all-products/"
OUTPUT_PATH = "data/product_urls.json"

def get_product_page_urls():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    print(f"Loading {INDEX_URL}...")
    driver.get(INDEX_URL)
    time.sleep(3)  # wait for JS to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    product_links = []
    for a in soup.select("a[href^='/products/']"):
        href = a.get("href")
        if any(key in href for key in ["overview", "resources", "integrate"]):
            full_url = BASE_URL + href
            if full_url not in product_links:
                product_links.append(full_url)

    return product_links

if __name__ == "__main__":
    print("Scraping product URLs...")
    urls = get_product_page_urls()
    print(f"✅ Found {len(urls)} product pages.")

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(urls, f, indent=2)

    print(f"✅ Saved to {OUTPUT_PATH}")
