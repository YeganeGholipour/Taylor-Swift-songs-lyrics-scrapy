from itemadapter import ItemAdapter
import psycopg2
from psycopg2 import sql

class SongscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        name = adapter.get('song_name')
        adapter['song_name'] = name.lower()
        return item

class SaveToPostgresPipeline:
    def __init__(self):
        self.conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='admin',
            database='songscraper'
        )
        self.cur = self.conn.cursor()

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS songs(
                id SERIAL PRIMARY KEY,
                song_name TEXT UNIQUE
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS lyrics(
                id SERIAL PRIMARY KEY,
                song_name TEXT,
                lyrics TEXT,
                url TEXT,
                UNIQUE(song_name)
            )
            """
        )

        self.conn.commit()

    def process_item(self, item, spider):
        try:
            if spider.name == 'songslistspider':
                self.cur.execute(
                    """
                    INSERT INTO songs (song_name)
                    VALUES (%s)
                    ON CONFLICT (song_name) DO NOTHING
                    """,
                    (item['song_name'],)
                )
            elif spider.name == 'taylorspider':
                self.cur.execute(
                    """
                    INSERT INTO lyrics (song_name, lyrics, url)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (song_name) DO NOTHING
                    """,
                    (item['song_name'], item['lyrics'], item['url'])
                )
            self.conn.commit()
        except psycopg2.Error as e:
            spider.logger.error(f"Error inserting item: {e}")
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
