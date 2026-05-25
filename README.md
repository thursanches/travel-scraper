# travel-scraper

Just a simple project that uses scraping to generate a CSV file containing hotel names, ratings, locations and prices from Booking.com.

---
## 🛠️ Tech Stack

* **Python 3.8+**
* **Playwright** (Async API for headless browser automation)
* **BeautifulSoup4** (Fast HTML parsing)
* **Pandas** (Data manipulation and CSV export)
* **python-dotenv** (Environment variable management)

---
Installing
```
pip install -r requirements.txt

playwright install chromium
```
Create a .env file in the root directory. Example:

BOOKING_URL="https://www.booking.com/parameter_of_searching"
