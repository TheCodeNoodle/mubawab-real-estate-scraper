from bs4 import BeautifulSoup
import requests
import time
import random
import json
import re

data_base = {}

# --- Helpers ---
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

# --- User input ---
def select_language():
    langs = ["fr", "en"]
    while True:
        try:
            choice = int(input("Languages:\n1- French\n2- English\n> "))
            if 1 <= choice <= 2:
                return langs[choice - 1]
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Enter a number.")

def select_city(language):
    cities = ["rabat", "tanger", "marrakech", "casablanca", "agadir"]
    print("-------------------------------------------------")
    for i, city in enumerate(cities, 1):
        print(f"{i}- {city.capitalize()}")
    prompt = "Choisissez la ville: " if language == "fr" else "Choose the city: "
   
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(cities):
                return cities[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(cities)}.")
        except ValueError:
            print("Invalid input. Enter a number.")

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

base_url = "https://www.mubawab.ma/"

# --- Scraper ---
def mub_scraper(data_base, base_url, language, city, page):
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
                return data_base
            
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
                        print(f"✓ Found listing:")
                        print(f"  Location: {location_text}")
                        print(f"  Title: {title_text}")
                        print(f"  Price: {price_int} DH")
                        if features:
                            print(f"  Features: {features}")
                        print("-" * 50)
                        
                        if location_text not in data_base:
                            data_base[location_text] = {}
                        data_base[location_text][title_text] = {
                            "price": price_int,
                            "area": features.get("area"),
                            "rooms": features.get("rooms"),
                            "bedrooms": features.get("bedrooms"),
                            "bathrooms": features.get("bathrooms")
                        }
                else:
                    print("⚠️ Incomplete listing found.")
                    
        else:
            print(f"Error {response.status_code}")
                
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return data_base

# --- Run program ---
print("--------Mubawab Scraper--------")
lang = select_language()
city = select_city(lang)

print(f"\nScraping {city.capitalize()} listings...")

page = 1
while True:
    prev_count = sum(len(listings) for listings in data_base.values())
    mub_scraper(data_base, base_url, lang, city, page)
    new_count = sum(len(listings) for listings in data_base.values())
    if new_count == prev_count:  # no new listings found
        break
    page += 1

# --- Print results ---
print("\n" + "="*60)
print(" "*18 + "---SCRAPED LISTINGS---")
print("="*60)

if data_base:
    file_name = f"data_{city}.json"
    with open(file_name, 'w', encoding="utf-8") as json_file:
        json.dump(data_base, json_file, indent=4, ensure_ascii=False)
    
    total_listings = sum(len(listings) for listings in data_base.values())
    print(f"Total listings found: {total_listings}")
    
    for location, listings in data_base.items():
        prices = [info["price"] for info in listings.values() if info["price"]]
        areas = [info["area"] for info in listings.values() if info["area"] and info["price"]]
        
        if prices:
            avg_price = sum(prices) / len(prices)
        else:
            avg_price = 0
        
        if areas:
            avg_ppm = sum(info["price"]/info["area"] for info in listings.values() if info["price"] and info["area"]) / len(areas)
        else:
            avg_ppm = 0
        
        print(f"\n📍 {location}")
        print("-" * len(f"📍 {location}"))
        print(f"   ➡ Average price: {avg_price:,.0f} DH")
        if avg_ppm:
            print(f"   ➡ Average price per m²: {avg_ppm:,.0f} DH/m²")
        
        for title, info in listings.items():
            print(f"\n  🏠 {title}")
            print(f"     💸 {info['price']:,} DH")
            if info["area"]:
                print(f"     📐 {info['area']} m²")
            if info["rooms"]:
                print(f"     🏡 {info['rooms']} rooms")
            if info["bedrooms"]:
                print(f"     🛏️ {info['bedrooms']} bedrooms")
            if info["bathrooms"]:
                print(f"     🛁 {info['bathrooms']} bathrooms")
else:
    print("❌ No data was scraped!")
