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

### 1. Clone the repository

```bash
git clone https://github.com/TheCodeNoodle/mubawab-real-estate-scraper.git
cd mubawab-real-estate-scraper
```

### 2. Install dependencies

Make sure you have Python 3 installed, then run:
```bash
pip install -r requirements.txt
```
Alternatively, install packages manually:
```bash
pip install requests beautifulsoup4
```
### 3. Run the scraper
```bash
python scraper.py
```
### 4. Follow the interactive prompts

  Select your preferred language (French or English)

  Choose a city from the available options (Rabat, Tanger, Marrakech, Casablanca, Agadir)

### 5. View the results

The scraper will print listings grouped by neighborhood directly in your terminal.
