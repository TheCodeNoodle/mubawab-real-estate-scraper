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

- `requests` – to fetch HTML content
- `BeautifulSoup` – to parse and extract data from HTML
- `random`, `time` – to randomize delays and avoid detection

---

## 📦 Example Output

```plaintext
📍 Hay Riad
  🏠 Spacious Apartment with Balcony
     💰 8,500 DH

📍 Agdal
  🏠 Modern Studio in City Center
     💰 5,200 DH
