# McMaster-Carr Steel Price Scraper

A Python web scraping script that extracts pricing and product information from McMaster-Carr's steel products page.

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Google Chrome** browser installed
3. **ChromeDriver** (will be installed automatically via webdriver-manager)

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, install manually:

```bash
pip install selenium webdriver-manager
```

## Usage

### Basic Usage

Run the script:

```bash
python scrape_mcmaster_steel.py
```

This will:
- Open a Chrome browser window
- Navigate to the McMaster-Carr steel products page
- Scrape product information (part numbers, prices, specifications)
- Print results to console
- Save data to a CSV file with timestamp

### Headless Mode

To run without opening a browser window, edit the script and change:

```python
scraper = McMasterSteelScraper(headless=True)
```

### Output

The script generates a CSV file named `mcmaster_steel_prices_YYYYMMDD_HHMMSS.csv` containing:
- Part Number
- Description
- Price
- Specifications
- Product Link

## Important Notes

### Website Structure

McMaster-Carr uses heavy JavaScript rendering, which means:
- The script requires Selenium (not just BeautifulSoup)
- Page load times may vary
- Selectors may need updates if the website changes

### Rate Limiting

Be respectful of McMaster-Carr's servers:
- Don't run the scraper too frequently
- Consider adding delays between requests if scraping multiple pages
- Check McMaster-Carr's Terms of Service and robots.txt

### Troubleshooting

**No products found:**
- Run with `headless=False` to see what's happening in the browser
- Check if the page structure has changed
- Increase wait times in the script

**ChromeDriver errors:**
- Make sure Chrome browser is installed
- The webdriver-manager should handle ChromeDriver automatically
- Update Chrome to the latest version

**Timeout errors:**
- Increase the timeout in `WebDriverWait` (currently 15 seconds)
- Check your internet connection
- The website might be slow or down

## Customization

### Adjust Timeouts

In [scrape_mcmaster_steel.py](scrape_mcmaster_steel.py):

```python
WebDriverWait(self.driver, 15)  # Change 15 to desired timeout in seconds
time.sleep(3)  # Adjust additional wait time
```

### Change Target URL

Modify the URL in the `__init__` method:

```python
self.url = "https://www.mcmaster.com/your-desired-url/"
```

### Update Selectors

If McMaster-Carr changes their HTML structure, update the CSS selectors in the `extract_product_data()` method.

## Legal Disclaimer

This script is for educational purposes. Before scraping any website:
- Review the website's Terms of Service
- Check the robots.txt file
- Respect rate limits and server resources
- Consider using official APIs if available

Web scraping may be against the terms of service of some websites. Use responsibly and at your own risk.
