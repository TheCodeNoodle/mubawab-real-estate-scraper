from bs4 import BeautifulSoup
import requests
import time
import random
import json
import re
import pandas as pd

# ----------------- Helpers -----------------
def clean_text(text: str) -> str:
    """Clean text (remove non-breaking spaces, extra whitespace)."""
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()

def extract_price(price_str: str):
    """Extract integer price from string like '24 000 000 DH'."""
    cleaned = price_str.replace("\xa0", " ").replace(",", ".")
    digits = re.sub(r"[^\d]", "", cleaned)  # keep only numbers
    return int(digits) if digits.isdigit() else None

def extract_features(item):
    """Extract area, rooms, bedrooms, bathrooms from the adDetailFeature section."""
    feature_map = {
        "icon-triangle": "area",
        "icon-house-boxes": "rooms",
        "icon-bed": "bedrooms",
        "icon-bath": "bathrooms"
    }
    features = {}
    for feat in item.select("div.adDetailFeature"):
        icon = feat.select_one("i")
        text = clean_text(feat.get_text())
        if not icon:
            continue
        icon_class = [cls for cls in icon.get("class", []) if cls.startswith("icon-")]
        if not icon_class:
            continue
        key = feature_map.get(icon_class[0])
        if key:
            num = re.findall(r"\d+", text)
            features[key] = int(num[0]) if num else None
    return features

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

# ----------------- Scraper -----------------
base_url = "https://www.mubawab.ma/"

def mub_scraper(base_url, language, city, page, data_list):
    url = f"{base_url}{language}/ct/{city}/immobilier-a-vendre-all:p:{page}"
    print(f"Requesting: {url}")
    
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        time.sleep(random.uniform(1, 3))
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            selectors_to_try = [
                "div.listingBox.feat",
                "div[class*='listingBox']",
                "div[class*='listing']",
                "article",
                ".property-item",
                ".listing-item"
            ]
            
            containers = []
            for selector in selectors_to_try:
                containers = soup.select(selector)
                if containers:
                    print(f"Found {len(containers)} containers using {selector} selector")
                    break
            
            if not containers:
                print("⚠️ No containers found.")
                return data_list
            
            for item in containers:
                price, title, location = None, None, None
                
                price_selectors = [
                    "span.priceTag.hardShadow.float-left",
                    "span[class*='price']",
                    ".price",
                    "[class*='prix']"
                ]
                for selector in price_selectors:
                    price = item.select_one(selector)
                    if price: break
                
                title_selectors = [
                    "h2.listingTit.col-11",
                    "h2[class*='listing']",
                    "h2", "h3", ".title",
                    "[class*='titre']"
                ]
                for selector in title_selectors:
                    title = item.select_one(selector)
                    if title: break
                
                location_selectors = [
                    "span.listingH3",
                    "span[class*='location']",
                    ".location",
                    "[class*='lieu']"
                ]
                for selector in location_selectors:
                    location = item.select_one(selector)
                    if location: break
                
                if title and price and location:
                    title_text = clean_text(title.get_text(strip=True))
                    location_text = clean_text(location.get_text(strip=True))
                    raw_price = price.get_text(strip=True)
                    price_int = extract_price(raw_price)
                    
                    features = extract_features(item)
                    
                    if price_int:
                        data_list.append({
                            "location": location_text,
                            "title": title_text,
                            "price": price_int,
                            "area": features.get("area"),
                            "rooms": features.get("rooms"),
                            "bedrooms": features.get("bedrooms"),
                            "bathrooms": features.get("bathrooms")
                        })
                else:
                    print("⚠️ Incomplete listing found.")
                    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return data_list

# ----------------- Run -----------------
print("--------Mubawab Scraper--------")
language = "fr"  # french is better, since the website is moroccan
city = "casablanca"  # choose the city directly, terminal inputs are just dumb

print(f"\nScraping {city.capitalize()} listings...")

data_list = []
page = 1
while True:
    prev_count = len(data_list)
    mub_scraper(base_url, language, city, page, data_list)
    new_count = len(data_list)
    if new_count == prev_count:  # no new listings found
        break
    page += 1

# ----------------- Save -----------------
if data_list:
    # Save JSON
    json_file = f"data_{city}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)
    
    # Save CSV
    df = pd.DataFrame(data_list)
    csv_file = f"data_{city}.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    
    print(f"\nSaved {len(df)} listings to {json_file} and {csv_file}")
else:
    print("!!__No data was scraped__!!")
