# ScrapyTests 

## Question 1

### Setup Commands

1. Create a virtual environment:
   ```
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```
   .\.venv\Scripts\Activate
   ```
   
3. Install the required packages:
   ```
   python -m pip install scrapy==2.4 shub scrapy-crawlera google-cloud-storage scrapy-sessions
   ```

4. Freeze the installed packages to requirements.txt:
   ```
   pip freeze > requirements.txt
   ```

### Installed Packages
- scrapy==2.4
- shub
- scrapy-crawlera
- google-cloud-storage
- scrapy-sessions

## Other Notes
- Needed to downgrade Python to 3.9.10 for compatibility with Scrapy 2.4
- Needed to downgrade some other packages as they were too new to be compatible with the Scrapy version
- `aaIndustrialProducts.json` is not the complete scrape as there was many products on the website and it was Scraping for quite a long time.
