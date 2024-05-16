# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SongscraperItem(scrapy.Item):
    song_name = scrapy.Field()

class TaylorScraperItem(scrapy.Item):
    song_name = scrapy.Field()
    lyrics = scrapy.Field()
    url = scrapy.Field()