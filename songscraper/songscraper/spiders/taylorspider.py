import scrapy
import psycopg2
import re
from urllib.parse import urlencode
from urllib.parse import urlencode, quote_plus
from songscraper.items import TaylorScraperItem


class TaylorspiderSpider(scrapy.Spider):
    name = "taylorspider"
    allowed_domains = ["genius.com"]
    start_urls = ["https://genius.com"]

    def parse(self, response):
        pass

    def start_requests(self):
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='admin',
            database='songscraper'
        )

        cur = conn.cursor()
        cur.execute('SELECT song_name FROM songs')
        songs = cur.fetchall()
        conn.close()

        for song in songs:
            song_name = song[0]
            formatted_song_name = song_name.lower().replace(' ', '-').replace("'", "")
            url = f"https://genius.com/Taylor-swift-{quote_plus(formatted_song_name)}-lyrics"
            yield scrapy.Request(url, callback=self.parse_lyrics, meta={'song_name': song_name})

    def parse_search_results(self, response):
        first_result = response.css('div.mini_card-info a::attr(href)').get()
        if first_result:
            yield response.follow(first_result, callback=self.parse_lyrics, meta=response.meta)

    def parse_lyrics(self, response):
        if response.status == 404:
            self.logger.warning(f"Page not found for {response.url}")
            return
        
        lyrics_item = TaylorScraperItem()
        song_name = response.meta['song_name']
        lyrics_div = response.css('div.Lyrics__Container-sc-1ynbvzw-1.kUgSbL')
        lyrics_text = lyrics_div.css('::text, a::text, span::text').getall() 
        lyrics_text = ' '.join(lyrics_text)

        lyrics_item['song_name'] = song_name
        lyrics_item['lyrics'] = lyrics_text
        lyrics_item['url'] = response.url

        return lyrics_item
    
    # def clean_lyrics(self, lyrics):
    #     # Remove [Verse], [Chorus], etc.
    #     lyrics = re.sub(r'\[.*?\]', '', lyrics)
    #     # Replace escaped unicode characters with a space
    #     lyrics = lyrics.replace('\u2005', ' ')
    #     # Replace multiple spaces with a single space
    #     lyrics = re.sub(r'\s+', ' ', lyrics)
    #     # Add line breaks after periods for readability (optional)
    #     lyrics = re.sub(r'(?<!\.\.\.)([.!?])', r'\1\n', lyrics)
    #     # Strip leading and trailing spaces
    #     lyrics = lyrics.strip()
    #     return lyrics

