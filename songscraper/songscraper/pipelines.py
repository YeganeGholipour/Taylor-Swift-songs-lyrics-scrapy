from itemadapter import ItemAdapter
import psycopg2
from psycopg2 import sql
import re

class SongscraperPipeline:
    def process_item(self, item, spider):
        if spider.name == 'songslistspider':
            adapter = ItemAdapter(item)
            name = adapter.get('song_name')
            adapter['song_name'] = name.lower()
            return item
        elif spider.name == 'taylorspider':
            adapter = ItemAdapter(item)
            lyrics = adapter.get('lyrics')
        
            # Remove [Verse], [Chorus], etc.
            lyrics = re.sub(r'\[.*?\]', '', lyrics)
            
            # Replace escaped unicode characters with a space
            lyrics = lyrics.replace('\u2005', ' ')
            
            # Replace escaped newline characters with actual newlines
            lyrics = lyrics.replace('\\n', '\n')

            # Decode any escaped characters like \'
            # lyrics = bytes(lyrics, "utf-8").decode("unicode_escape")
            
            # Add line breaks after periods, question marks, and exclamation marks for readability
            lyrics = re.sub(r'(?<!\.\.\.)([.!?])', r'\1\n', lyrics)
            
            # Ensure there is a space after punctuation if a word follows immediately
            lyrics = re.sub(r'([.!?])([A-Za-z])', r'\1 \2', lyrics)
            
            # Replace multiple spaces with a single space
            lyrics = re.sub(r'\s+', ' ', lyrics)
            
            # Replace multiple newlines with a single newline
            lyrics = re.sub(r'\n+', '\n', lyrics)

            # Replace escaped single quotes with regular single quotes
            lyrics = lyrics.replace("\\ '", "'")
            
            # Remove backslashes
            lyrics = lyrics.replace('\\', '')
            
            # Remove forward slashes
            lyrics = lyrics.replace('/', '')
            # Strip leading and trailing spaces
            lyrics = lyrics.strip()


            adapter['lyrics'] = lyrics
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
