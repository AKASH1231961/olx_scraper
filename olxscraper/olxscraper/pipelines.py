# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter

class OlxscraperPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("olx_data.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                property_name TEXT,
                property_id TEXT,
                breadcrumbs TEXT,
                price TEXT,
                image_url TEXT,
                description TEXT,
                seller_name TEXT,
                location TEXT,
                property_type TEXT,
                bathrooms INTEGER,
                bedrooms INTEGER
            )
        """)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO listings (
                property_name, property_id, breadcrumbs, price, image_url,
                description, seller_name, location, property_type,
                bathrooms, bedrooms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get('property_name'),
            item.get('property_id'),
            ", ".join(item.get('breadcrumbs', [])),
            item.get('price'),
            item.get('image_url'),
            item.get('description'),
            item.get('seller_name'),
            item.get('location'),
            item.get('property_type'),
            item.get('bathrooms'),
            item.get('bedrooms')
        ))
        return item
