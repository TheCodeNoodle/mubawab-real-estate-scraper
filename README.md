# Mubawab Real Estate Scraper

A Python web scraper for extracting real estate listings from Mubawab.ma, Morocco's leading property website. This tool allows you to collect property data from multiple cities and analyze market trends.

## Features

- **Multi-language Support**: Scrape in French or English
- **Multi-city Coverage**: Support for 5 major Moroccan cities
- **Comprehensive Data Extraction**: Price, location, area, rooms, bedrooms, bathrooms
- **Automatic Pagination**: Scrapes multiple pages until no new listings are found
- **Data Export**: Saves results to JSON files
- **Market Analysis**: Calculates average prices and price per square meter
- **Robust Error Handling**: Handles network errors and missing data gracefully

## Supported Cities

- Rabat
- Tanger (Tangier)
- Marrakech
- Casablanca
- Agadir

## Requirements

```bash
pip install beautifulsoup4 requests
```

## Installation

1. Clone or download the script
2. Install required dependencies:
   ```bash
   pip install beautifulsoup4 requests
   ```
3. Run the script:
   ```bash
   python Scraper - Mubawab.py
   ```

## Usage

1. **Select Language**: Choose between French (1) or English (2)
2. **Select City**: Pick from the 5 available cities
3. **Wait for Scraping**: The script will automatically scrape all available pages
4. **View Results**: See scraped data in terminal and exported JSON file

### Example Run

```
--------Mubawab Scraper--------
Languages:
1- French
2- English
> 1
-------------------------------------------------
1- Rabat
2- Tanger
3- Marrakech
4- Casablanca
5- Agadir
Choisissez la ville: 1

Scraping Rabat listings...
```

## Output

The scraper provides two types of output:

### 1. Terminal Output
- Real-time scraping progress
- Individual listing details
- Summary statistics by location
- Average prices and price per m²

### 2. JSON File
- Structured data saved as `data_{city}.json`
- Organized by location and property title
- Complete property details for further analysis

### Sample Output Structure

```json
{
  "Rabat Centre": {
    "Appartement 3 chambres": {
      "price": 2500000,
      "area": 120,
      "rooms": 4,
      "bedrooms": 3,
      "bathrooms": 2
    }
  }
}
```

## Data Fields

| Field | Description |
|-------|-------------|
| `price` | Property price in Moroccan Dirhams (DH) |
| `area` | Property area in square meters (m²) |
| `rooms` | Total number of rooms |
| `bedrooms` | Number of bedrooms |
| `bathrooms` | Number of bathrooms |

## Technical Details

### Web Scraping Strategy
- **Respectful Scraping**: Includes random delays (1-3 seconds) between requests
- **Multiple Selectors**: Uses fallback CSS selectors for robust data extraction
- **User-Agent Rotation**: Mimics real browser requests
- **Error Handling**: Graceful handling of network timeouts and parsing errors

### Rate Limiting
- Random delays between requests to avoid overwhelming the server
- Timeout handling for network requests
- Respectful scraping practices

## Limitations

- **Website Dependency**: Functionality depends on Mubawab.ma's HTML structure
- **Rate Limiting**: May need to adjust delays for heavy usage
- **Geographic Scope**: Limited to 5 major Moroccan cities
- **Data Completeness**: Some listings may have incomplete information

## Legal and Ethical Considerations

- **Personal Use**: Intended for personal research and analysis
- **Data Usage**: Respect the website's terms of service
- **Rate Limits**: Don't overload the server with requests

## Troubleshooting

### Common Issues

1. **No Data Scraped**
   - Check internet connection
   - Website structure may have changed
   - Try different city/language combination

2. **Request Timeouts**
   - Increase timeout value in requests.get()
   - Check network stability

3. **Parsing Errors**
   - Website HTML structure may have changed
   - Update CSS selectors if needed

### Error Messages

- `⚠️ No containers found`: No listings found on the page
- `⚠️ Incomplete listing found`: Some required fields are missing
- `Request failed`: Network connection issue

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the scraper's functionality.

## Disclaimer

This tool is for educational and research purposes. Users are responsible for complying with Mubawab.ma's terms of service and applicable laws. The authors are not responsible for any misuse of this tool.

## License

This project is open source. Please use responsibly and ethically.
