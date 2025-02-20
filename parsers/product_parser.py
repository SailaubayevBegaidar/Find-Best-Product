import requests
from bs4 import BeautifulSoup
import json
import time
import random
from app import mongo
from datetime import datetime
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

WEBSITE_CONFIGS = {
    'amazon': {
        'name_selector': '#productTitle',
        'price_selector': '.a-price-whole',
        'category_selector': '.nav-a-content'
    },
    'ebay': {
        'name_selector': '.x-item-title',
        'price_selector': '.x-price-primary',
        'category_selector': '.breadcrumbs'
    },
    'walmart': {
        'name_selector': '.prod-ProductTitle',
        'price_selector': '.price-characteristic',
        'category_selector': '.breadcrumb'
    }
}

def get_website_config(url):
    domain = urlparse(url).netloc
    for site, config in WEBSITE_CONFIGS.items():
        if site in domain:
            return config
    return None

def scrape_product_data(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        config = get_website_config(url)
        if not config:
            raise ValueError(f"Unsupported website: {url}")

        soup = BeautifulSoup(response.text, "html.parser")
        
        product_data = {
            "name": None,
            "price": None,
            "category": None,
            "url": url,
            "source": urlparse(url).netloc,
            "last_updated": datetime.utcnow(),
            "available": True
        }

        # Extract data using site-specific selectors
        try:
            name_elem = soup.select_one(config['name_selector'])
            if name_elem:
                product_data["name"] = name_elem.get_text().strip()

            price_elem = soup.select_one(config['price_selector'])
            if price_elem:
                price_text = price_elem.get_text().strip()
                # Remove currency symbols and convert to float
                price = float(''.join(filter(str.isdigit, price_text)))
                product_data["price"] = price

            category_elem = soup.select_one(config['category_selector'])
            if category_elem:
                product_data["category"] = category_elem.get_text().strip()
        except Exception as e:
            print(f"Error extracting data: {e}")

        # Validate required fields
        if not product_data["name"] or not product_data["price"]:
            raise ValueError("Required fields missing")

        # Store in database
        mongo.db.products.update_one(
            {"url": url},
            {"$set": product_data},
            upsert=True
        )

        return product_data

    except requests.RequestException as e:
        print(f"Network error for {url}: {e}")
        return None
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def batch_scrape_products(urls, delay_range=(2, 5)):
    results = []
    for url in urls:
        try:
            product = scrape_product_data(url)
            if product:
                results.append(product)
            
            delay = random.uniform(*delay_range)
            print(f"Waiting {delay:.2f} seconds before next request...")
            time.sleep(delay)
            
        except Exception as e:
            print(f"Failed to process {url}: {e}")
            continue
    
    return results

if __name__ == "__main__":
    input_file = "generated_urls.json"
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            urls = json.load(f).get("urls", [])
        
        results = batch_scrape_products(urls)
        print(f"Successfully scraped {len(results)} products out of {len(urls)} URLs")
        
    except FileNotFoundError:
        print(f"Input file {input_file} not found")
    except json.JSONDecodeError:
        print(f"Invalid JSON in {input_file}")
    except Exception as e:
        print(f"Unexpected error: {e}")
