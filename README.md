# AmbitionBox Company Scraper

A robust and scalable web scraping project built using **Python**, **Requests**, **BeautifulSoup**, and **JSON parsing** to extract structured company insights from AmbitionBox.

This scraper collects company information such as:
- Company Name
- Company Profile URL
- Overall Rating
- Total Reviews
- Industry Tags
- Company Description
- Salary Rating
- Job Security Rating
- Work-Life Balance Rating

The project follows a hybrid scraping approach:
- **HTML parsing** for listing pages
- **Structured JSON extraction (`__NEXT_DATA__`)** for company detail pages

This makes the scraper:
- More reliable
- Faster
- Easier to maintain
- Less dependent on unstable frontend class names

---

# Features

- Scrapes 50 companies
- Extracts structured company data
- Uses `requests.Session()` for efficient networking
- Retry-safe request handling
- Duplicate company prevention
- Random delays to reduce blocking
- Saves data in:
  - CSV format
  - JSON format
- Clean modular code structure
- Production-style scraper architecture

---

# Tech Stack

- Python 3
- Requests
- BeautifulSoup4
- Pandas
- JSON

---

# Project Structure

```text
ambitionbox_scraper/
│
├── scraper.py
├── companies.csv
├── companies.json
├── README.md
└── requirements.txt
```

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd ambitionbox_scraper
```

---

## 2. Create Virtual Environment

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

Create a `requirements.txt` file with:

```text
requests
beautifulsoup4
pandas
```

---

# How It Works

## Step 1 — Scrape Listing Pages

The scraper visits:

```text
https://www.ambitionbox.com/list-of-companies?page=1
```

and extracts:
- Company Name
- Company URL

using BeautifulSoup.

---

## Step 2 — Scrape Company Detail Pages

Each company page contains a hidden structured JSON object:

```html
<script id="__NEXT_DATA__">
```

The scraper parses this JSON to extract:
- Ratings
- Reviews
- Industry Information
- Description
- Metadata

This approach is more stable than scraping frontend HTML classes.

---

# Output Files

## companies.csv

Structured tabular dataset.

## companies.json

JSON formatted company dataset.

---

# Sample Output

| Company Name | Overall Rating | Total Reviews | Salary Rating |
|---|---|---|---|
| TCS | 3.3 | 1.1L | 2.5 |
| Accenture | 3.7 | 73.5k | 3.3 |
| Wipro | 3.6 | 65.1k | 3.0 |

---

# Anti-Blocking Measures

The scraper includes:
- Rotating delays
- Session handling
- Retry mechanism
- Timeout handling

to reduce the chances of request blocking.

---

# Key Learning Outcomes

This project demonstrates:
- Real-world web scraping
- HTML parsing
- JSON data extraction
- Data cleaning
- CSV/JSON generation
- Modular scraper design
- Error handling
- Scalable scraping architecture

---

# Future Improvements

Possible enhancements:
- Selenium integration for dynamic pages
- Proxy rotation
- Async scraping
- Database integration
- Dashboard visualization
- REST API layer

---

# Disclaimer

This project was built for educational and internship assessment purposes only.

Please respect:
- Website Terms of Service
- robots.txt policies
- Responsible scraping practices

---

# Author

**Samridhi Choudhary**  
B.Tech Computer Science (Data Science)  
Bennett University
