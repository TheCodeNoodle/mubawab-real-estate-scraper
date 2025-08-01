from bs4 import BeautifulSoup
import requests
import time
import random

data_base = {}

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
    if language == "fr":
        prompt = "Choisissez la ville: "
    else: 
        "Choose the city: "
   
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
    #--------Return headers to mimic a real browser--------
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

base_url = "https://www.mubawab.ma/"

def mub_scraper(data_base, base_url, language, city):
    url = f"{base_url}{language}/t/{city}"
    print(f"Requesting: {url}")
    
    try:
        #--------Add headers and delay to avoid detection--------
        response = requests.get(url, headers=get_headers(), timeout=10)
        time.sleep(random.uniform(1, 3))
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            
            #--------Try multiple possible selectors for listings--------
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
                print("No containers found. Let's examine the page structure...")
                #--------Print first 2000 characters to see structure--------
                print("Page content preview:")
                print(response.text[:2000])
                return data_base
            
            #--------Try different selectors for price, title, location--------
            for item in containers:
                price = None
                title = None
                location = None
                
                #--------Try multiple selectors for price--------
                price_selectors = [
                    "span.priceTag.hardShadow.float-left",
                    "span[class*='price']",
                    ".price",
                    "[class*='prix']"
                ]
                
                for selector in price_selectors:
                    price = item.select_one(selector)
                    if price:
                        break
                
                #--------Try multiple selectors for title--------
                title_selectors = [
                    "h2.listingTit.col-11",
                    "h2[class*='listing']",
                    "h2",
                    "h3",
                    ".title",
                    "[class*='titre']"
                ]
                
                for selector in title_selectors:
                    title = item.select_one(selector)
                    if title:
                        break
                
                #--------Try multiple selectors for location--------
                location_selectors = [
                    "span.listingH3",
                    "span[class*='location']",
                    ".location",
                    "[class*='lieu']"
                ]
                
                for selector in location_selectors:
                    location = item.select_one(selector)
                    if location:
                        break
                
                if title and price and location:
                    title_text = title.get_text(strip=True)
                    price_text = price.get_text(strip=True)
                    location_text = location.get_text(strip=True)
                    
                    print(f"✓ Found listing:")
                    print(f"  Location: {location_text}")
                    print(f"  Title: {title_text}")
                    print(f"  Price: {price_text}")
                    print("-" * 50)
                    
                    if location_text not in data_base:
                        data_base[location_text] = {}
                    data_base[location_text][title_text] = price_text
                else:
                    #--------Debug: show what we found--------
                    print("⚠️  Incomplete listing found:")
                    if title:
                        print(f"  Title: {title.get_text(strip=True)}")
                    if price:
                        print(f"  Price: {price.get_text(strip=True)}")
                    if location:
                        print(f"  Location: {location.get_text(strip=True)}")
                    print("-" * 30)
                    
        else:
            print(f"Error {response.status_code}")
            if response.status_code == 403:
                print("Access forbidden!")
            elif response.status_code == 404:
                print("Page not found!")
                
    except requests.exceptions.RequestException as awd: #------My fancy variable naming------
        print(f"Request failed: {awd}")
    except Exception as awd:
        print(f"An error occurred: {awd}")
    
    return data_base

#--------Run program--------
print("--------Mubawab Scraper--------")
lang = select_language()
city = select_city(lang)

print(f"\nScraping {city.capitalize()} listings...")
mub_scraper(data_base, base_url, lang, city)

#--------Print results--------
print("\n" + "="*60)
print(" "*18 + "---SCRAPED LISTINGS---")
print("="*60)

if data_base:
    total_listings = sum(len(listings) for listings in data_base.values())
    print(f"Total listings found: {total_listings}")
    
    for location, listings in data_base.items():
        print(f"\n📍 {location}")
        print("-" * len(f"📍 {location}"))
        for title, price in listings.items():
            print(f"  🏠 {title}")
            print(f"     💸 {price}")
            print()
else:
    print("❌ No data was scraped!")