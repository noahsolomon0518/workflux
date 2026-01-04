"""
McMaster-Carr Steel Products Price Scraper

This script scrapes pricing and product information from McMaster-Carr's steel products page.
Note: McMaster-Carr uses heavy JavaScript, so Selenium is required for proper rendering.
"""

import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class McMasterSteelScraper:
    def __init__(self, headless=True):
        """Initialize the scraper with Chrome WebDriver."""
        self.url = "https://www.mcmaster.com/products/metals/steel-2~/"
        self.chrome_options = Options()

        if headless:
            self.chrome_options.add_argument("--headless")

        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")

        self.driver = None
        self.products = []

    def start_driver(self):
        """Start the Chrome WebDriver."""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            print("Chrome WebDriver started successfully")
        except Exception as e:
            print(f"Error starting Chrome WebDriver: {e}")
            print("Make sure you have Chrome and ChromeDriver installed")
            raise

    def scrape_products(self):
        """Scrape product information from the page."""
        if not self.driver:
            raise RuntimeError("WebDriver not started. Call start_driver() first.")

        print(f"Loading page: {self.url}")
        self.driver.get(self.url)

        # Wait for page to load - adjust timeout as needed
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ItmTbl"))
            )
            print("Page loaded successfully")
        except TimeoutException:
            print("Timeout waiting for product table. The page structure might have changed.")
            print("Current page title:", self.driver.title)

        # Additional wait for JavaScript to render
        time.sleep(3)

        # Try to find product rows
        try:
            print(self.driver.page_source)
            product_rows = self.driver.find_elements(By.CSS_SELECTOR, ".ItmTblRow, tr[class*='ItmTbl']")
            print(f"Found {len(product_rows)} potential product rows")

            for row in product_rows:
                try:
                    product_data = self.extract_product_data(row)
                    if product_data:
                        self.products.append(product_data)
                except Exception as e:
                    print(f"Error extracting product data from row: {e}")
                    continue

        except NoSuchElementException:
            print("Could not find product rows. Trying alternative selectors...")
            self.try_alternative_selectors()

        print(f"Successfully scraped {len(self.products)} products")
        return self.products

    def extract_product_data(self, row_element):
        """Extract product data from a table row element."""
        product = {}

        try:
            # Extract part number
            part_number_elem = row_element.find_element(By.CSS_SELECTOR, ".PartNbr, [class*='PartNbr']")
            product['part_number'] = part_number_elem.text.strip()
        except NoSuchElementException:
            product['part_number'] = "N/A"

        try:
            # Extract price
            price_elem = row_element.find_element(By.CSS_SELECTOR, ".ItmTblCellPrce, [class*='Price'], [class*='Prce']")
            product['price'] = price_elem.text.strip()
        except NoSuchElementException:
            product['price'] = "N/A"

        try:
            # Extract specifications
            spec_elems = row_element.find_elements(By.CSS_SELECTOR, ".ItmTblCellSpec, [class*='Spec']")
            product['specifications'] = " | ".join([spec.text.strip() for spec in spec_elems if spec.text.strip()])
        except NoSuchElementException:
            product['specifications'] = "N/A"

        try:
            # Extract product description/name
            desc_elem = row_element.find_element(By.CSS_SELECTOR, "a, .ItmTblLnk")
            product['description'] = desc_elem.text.strip()
            product['link'] = desc_elem.get_attribute('href')
        except NoSuchElementException:
            product['description'] = "N/A"
            product['link'] = "N/A"

        # Only return product if we have at least some data
        if any(v != "N/A" for v in product.values()):
            return product
        return None

    def try_alternative_selectors(self):
        """Try alternative methods to find products if primary method fails."""
        print("Attempting to scrape with alternative selectors...")

        # Try finding all links or table cells
        try:
            all_cells = self.driver.find_elements(By.TAG_NAME, "td")
            print(f"Found {len(all_cells)} table cells")

            # Look for cells that might contain prices (contain $ symbol)
            price_pattern_cells = [cell for cell in all_cells if '$' in cell.text]
            print(f"Found {len(price_pattern_cells)} cells with price indicators")

        except Exception as e:
            print(f"Alternative selector attempt failed: {e}")

    def save_to_csv(self, filename=None):
        """Save scraped products to CSV file."""
        if not self.products:
            print("No products to save")
            return

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mcmaster_steel_prices_{timestamp}.csv"

        fieldnames = ['part_number', 'description', 'price', 'specifications', 'link']

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.products)

        print(f"Data saved to {filename}")
        return filename

    def print_products(self):
        """Print products to console."""
        if not self.products:
            print("No products found")
            return

        for i, product in enumerate(self.products, 1):
            print(f"\n--- Product {i} ---")
            for key, value in product.items():
                print(f"{key}: {value}")

    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            print("WebDriver closed")


def main():
    """Main execution function."""
    scraper = McMasterSteelScraper(headless=False)  # Set to True to run without browser window

    try:
        scraper.start_driver()
        products = scraper.scrape_products()

        if products:
            scraper.print_products()
            scraper.save_to_csv()
        else:
            print("\nNo products were scraped. Possible reasons:")
            print("1. The page structure has changed")
            print("2. JavaScript didn't render properly")
            print("3. The selectors need to be updated")
            print("\nTry running with headless=False to see what's happening")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        scraper.close()


if __name__ == "__main__":
    main()
