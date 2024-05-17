# Taylor-Swift-songs-lyrics-scrapy

## Song Scraper

Song Scraper is a web scraping project built using Scrapy to extract song lyrics from Genius.com for a specified artist (in this case, Taylor Swift) and store them in a PostgreSQL database.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/song-scraper.git
```

2. Install dependencies:

```bash
cd song-scraper
pip install -r requirements.txt
```

3. Set up the PostgreSQL database:

    Make sure PostgreSQL is installed on your system.
    Create a database named songscraper.
    Update the database connection details in songscraper/settings.py if necessary.

## Usage

    1. Run the spiders to scrape Taylor Swift's song list from Wikipedia and fetch lyrics from Genius:

    ```bash
    scrapy crawl songslistspider
    scrapy crawl taylorspider
    ```

    2. Check the PostgreSQL database to verify the scraped data.

## Project Structure
songscraper/
│
├── songscraper/
│   ├── spiders/
│   │   ├── __init__.py
│   │   ├── songslistspider.py   # Spider to scrape Taylor Swift's song list from Wikipedia
│   │   └── taylorspider.py      # Spider to fetch song lyrics from Genius
│   ├── items.py                 # Scrapy items definition
│   ├── middlewares.py           # Custom Scrapy middlewares
│   ├── pipelines.py             # Scrapy pipelines for processing and storing data
│   ├── settings.py              # Scrapy project settings
│   └── __init__.py
│
├── scrapy.cfg                   # Scrapy configuration file
│
└── README.md                    # Project README file
