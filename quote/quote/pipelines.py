# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
# Extracted data > temporary containers (items) > database

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class QuotePipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()


    def create_connection(self):
        self.connection = sqlite3.connect("quotes.db")
        self.cursor = self.connection.cursor()
    

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS quotes_tb""")
        self.cursor.execute("""create table quotes_tb
                            (
                                quote text,
                                author text,
                                tag text
                            )""")


    def store_db(self, item):
        self.cursor.execute("""INSERT INTO quotes_tb VALUES(?, ?, ?)""", (item['quote'][0], item['author'][0], item['tag'][0]))
        
        
        self.connection.commit()


    def process_item(self, item, spider):
        self.store_db(item)

        return item
