# 🏘️ Mubawab Real Estate Scraper (Morocco)

A Python web scraper that extracts real estate listings (titles, prices, locations) from [Mubawab.ma](https://www.mubawab.ma), one of Morocco's leading property platforms.

This script supports both **French** and **English**, allows **city selection**, and includes multiple scraping protections such as dynamic selector fallbacks, fake headers, and randomized delays to simulate human behavior.

---

## 🚀 Features

- ✅ Language selection (French or English interface)  
- ✅ City selection (Rabat, Tanger, Marrakech, Casablanca, Agadir)  
- ✅ Handles changing website structure with selector fallbacks  
- ✅ Anti-bot detection techniques (User-Agent spoofing + delays)  
- ✅ Error handling for network and page structure issues  
- ✅ Outputs results by location with nested structure  

---

## 🧰 Tech Used

- `requests` – for sending HTTP requests  
- `BeautifulSoup` – for parsing and navigating HTML  
- `random`, `time` – for delays to mimic human behavior  

---

## 📦 Example Output

```plaintext
📍 Hay Riad
  🏠 Spacious Apartment with Balcony
     💰 8,500 DH

📍 Agdal
  🏠 Modern Studio in City Center
     💰 5,200 DH
```
## 🛠️ How to Use
#   1. Clone the Repository
```plaintext
git clone https://github.com/yourusername/mubawab-real-estate-scraper.git
cd mubawab-real-estate-scraper
```
#   2. Install Dependencies

Make sure you have Python 3 installed. Then run:

pip install requests beautifulsoup4

#   3. Run the Script

python scraper.py

#   4. Follow the Prompts

    Choose your interface language (French or English)

    Select a city from the list (Rabat, Tanger, etc.)

#   5. View the Output

Listings are grouped by location and printed in the terminal.
