import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
from telegram import Bot
import re
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Read data from the .env file
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Raise an error if TOKEN or CHAT_ID is not found in the .env file
if not TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN or CHAT_ID not found in the .env file. Please check the .env file.")

# Telegram bot configuration
bot = Bot(token=TOKEN)

# Fetch data from Amazon (with pagination)
async def parse_amazon(query):
    base_url = f'https://www.amazon.com/s?k={query.replace(" ", "+")}&page='
    all_data = []
    page_num = 1
    max_pages = 1  # Initially set to 1, will be determined later

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            })

            # Load the first page and determine the total number of pages
            url = f"{base_url}{page_num}"
            print(f"Loading page {page_num}: {url}")
            await page.goto(url)
            await page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=10000)
            await page.wait_for_timeout(5000)

            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')

            # Determine the total number of pages
            pagination_items = soup.find_all('span', class_='s-pagination-item')
            if pagination_items:
                # Get the last numeric element (usually the last page number)
                for item in pagination_items[::-1]:  # Check in reverse order
                    text = item.text.strip()
                    if text.isdigit():
                        max_pages = int(text)
                        break
            print(f"Total number of pages: {max_pages}")

            while page_num <= max_pages:
                if page_num > 1:  # First page is already loaded
                    url = f"{base_url}{page_num}"
                    print(f"Loading page {page_num}: {url}")
                    await page.goto(url)
                    await page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=10000)
                    await page.wait_for_timeout(5000)
                    content = await page.content()
                    soup = BeautifulSoup(content, 'html.parser')

                products = soup.find_all('div', {'data-component-type': 's-search-result'})
                print(f"Number of products found on page {page_num}: {len(products)}")

                for product in products:
                    # Product name
                    name_tag = product.find('h2', class_='a-size-medium a-spacing-none a-color-base a-text-normal')
                    name = name_tag['aria-label'] if name_tag and 'aria-label' in name_tag.attrs else "Unknown"

                    # Fetch price (using multiple methods)
                    price = "Price not available"
                    price_tag = product.find('span', class_='a-price')
                    if price_tag:
                        offscreen_price = price_tag.find('span', class_='a-offscreen')
                        if offscreen_price:
                            price = offscreen_price.text.strip()
                        else:
                            whole = price_tag.find('span', class_='a-price-whole')
                            fraction = price_tag.find('span', class_='a-price-fraction')
                            if whole and fraction:
                                price = f"${whole.text.strip()}.{fraction.text.strip()}"
                            elif whole:
                                price = f"${whole.text.strip()}"
                    else:
                        color_base = product.find('span', class_='a-color-base')
                        if color_base:
                            price_text = color_base.text.strip()
                            if re.match(r'^\$\d+(\.\d+)?$', price_text):
                                price = price_text

                    # Clean the price (keep only numbers and decimal points)
                    if price != "Price not available":
                        price = re.sub(r'[^\d\.]', '', price)
                        if not price:
                            price = "Price not available"

                    # Rating
                    rating = product.find('span', class_='a-icon-alt')
                    rating = rating.text.strip() if rating else "No rating"

                    # Fetch image URL
                    image = product.find('img', class_='s-image')
                    image_url = image['src'] if image and 'src' in image.attrs else "Image not available"

                    # Source
                    source = url

                    all_data.append({'name': name, 'price': price, 'rating': rating, 'image_url': image_url, 'source': source})

                page_num += 1

            await browser.close()
            print(f"Total number of products collected: {len(all_data)}")
            return all_data
    except Exception as e:
        print(f"Error while fetching data: {e}")
        return []

# Save data to a CSV file (with a query-based filename)
def save_to_csv(data, query):
    if data:
        # Create a safe filename based on the query
        safe_query = query.replace(" ", "_").lower()
        filename = f"{safe_query}_data.csv"
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        return filename
    return None

# Send the CSV file to Telegram
async def send_csv(chat_id, filename):
    try:
        with open(filename, 'rb') as file:
            await bot.send_document(chat_id=chat_id, document=file)
    except Exception as e:
        print(f"Error while sending the CSV file: {e}")

# Main function
async def main():
    # List of queries
    queries = ["laptop", "phone charger", "cooler"]

    for query in queries:
        print(f"\nCollecting data for query: {query}")
        data = await parse_amazon(query)
        if not data:
            await bot.send_message(chat_id=CHAT_ID, text=f"An error occurred while fetching data for the query: {query}.")
            continue

        filename = save_to_csv(data, query)
        if filename:
            await send_csv(CHAT_ID, filename)
        else:
            await bot.send_message(chat_id=CHAT_ID, text=f"No products found for the query: {query}.")

if __name__ == '__main__':
    asyncio.run(main())