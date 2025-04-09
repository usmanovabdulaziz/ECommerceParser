**Amazon Scraper Telegram Bot**

**Description**  
This project is a Python-based web scraper that extracts product data from Amazon and sends the results to a Telegram chat. It searches for products based on predefined queries, collects details such as product name, price, rating, and image URL, saves the data to CSV files, and delivers them via a Telegram bot.

**Features**  
- Scrapes product data from Amazon with pagination support.  
- Extracts product details including name, price, rating, and image URL.  
- Saves scraped data to CSV files (one file per query).  
- Sends CSV files to a specified Telegram chat.  
- Configurable via environment variables for secure API key management.

**Installation**  
Follow these steps to set up the project locally:  

1. Clone the repository:  
   ```
   git clone https://github.com/usmanovabdulaziz/ECommerceParser.git
   ```

2. Navigate to the project directory:  
   ```
   cd eccomerce_parsing
   ```

3. Create a virtual environment (optional but recommended):  
   ```
   python -m venv venv
   source venv/bin/activate
   # On Windows: venv\Scripts\activate
   ```

4. Install the required dependencies:  
   ```
   pip install -r requirements.txt
   ```

5. Run the script:  
   ```
   python amazon_scraper.py
   ```

**Usage**  
1. Start the script by running the command shown above.  
2. The script will scrape product data from Amazon based on the predefined queries (e.g., "laptop", "phone charger", "cooler").  
3. For each query, the script will:  
   - Save the scraped data to a CSV file (e.g., `laptop_data.csv`).  
   - Send the CSV file to the Telegram chat specified in the `.env` file.  

**Note**: Each time the script runs, the CSV files for the same query will be overwritten with the new data. For example, running the script multiple times with the query "laptop" will overwrite `laptop_data.csv` with the latest data.

**Example Output**  
- **Query**: "laptop"  
- **CSV File**: `laptop_data.csv`  
- **Content**:  
  ```
  name,price,rating,image_url,source
  "Example Laptop","599.99","4.5 out of 5 stars","https://example.com/image.jpg","https://www.amazon.com/s?k=laptop&page=1"
  ```

**Configuration**  
The script requires API keys for Telegram and a chat ID to send the CSV files. These are managed securely using a `.env` file:  

1. Create a `.env` file in the project root with the following content:  
   ```
   TELEGRAM_TOKEN=your_telegram_bot_api_key
   CHAT_ID=your_chat_id
   ```

2. Replace `your_telegram_bot_api_key` with the token provided by BotFather on Telegram.  
3. Replace `your_chat_id` with the ID of the Telegram chat where the bot will send the CSV files.  

The `.env` file is automatically loaded when you run `amazon_scraper.py`.

**Dependencies**  
- Python 3.8+  
- `playwright` - For web scraping.  
- `beautifulsoup4` - For HTML parsing.  
- `pandas` - For saving data to CSV files.  
- `python-telegram-bot` - For interacting with the Telegram API.  
- `python-dotenv` - For loading environment variables from `.env`.  

Install these dependencies with:  
```
pip install playwright beautifulsoup4 pandas python-telegram-bot python-dotenv
```

A full list of dependencies is available in `requirements.txt`.

**Contributing**  
Contributions are welcome! Feel free to submit a pull request or open an issue on GitHub. Please ensure your code follows PEP 8 style guidelines.

**License**  
This project is licensed under the MIT License. See the `LICENSE` file for more details.

**Contact**  
For questions or feedback, find me on GitHub: https://github.com/usmanovabdulaziz.
