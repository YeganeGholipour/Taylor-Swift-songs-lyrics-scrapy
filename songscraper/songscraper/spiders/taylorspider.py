import scrapy
import psycopg2
from urllib.parse import urlencode
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
            query = urlencode({'q': f'Taylor Swift {song_name}'})
            url = f"https://genius.com/search?{query}"
            yield scrapy.Request(url, callback=self.parse_search_results, meta={'song_name': song_name})

    def parse_search_results(self, response):
        first_result = response.css('div.mini_card-info a::attr(href)').get()
        if first_result:
            yield response.follow(first_result, callback=self.parse_lyrics, meta=response.meta)

    def parse_lyrics(self, response):
        lyrics_item = TaylorScraperItem()
        song_name = response.meta['song_name']
        lyrics_div = response.css('div.Lyrics__Container-sc-1ynbvzw-1.kUgSbL')
        lyrics_text = lyrics_div.css('::text, a::text, span::text').getall() 
        lyrics_text = ''.join(lyrics_text).strip()

        lyrics_item['song_name'] = song_name
        lyrics_item['lyrics'] = lyrics_text
        lyrics_item['url'] = response.url

        return lyrics_item

