import scrapy
from songscraper.items import SongscraperItem

class SongslistspiderSpider(scrapy.Spider):
    name = "songslistspider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_songs_by_Taylor_Swift#Notes"]

    def parse(self, response):
        for row in response.css('table.wikitable tbody tr'):
            song_name = row.css('th a::text').get()
            if song_name:
                songs_item = SongscraperItem()
                songs_item['song_name'] = song_name
                yield songs_item
                
