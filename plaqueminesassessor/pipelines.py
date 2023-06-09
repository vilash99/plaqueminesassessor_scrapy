# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PlaqueminesassessorPipeline:
    def process_item(self, item, spider):
        return item


class SaveToPostgreSQLPipeline:
    def __init__(self):
        # Connection Details
        hostname = 'localhost'
        database = 'plaque'
        username = 'postgres'
        password = '****' # use database password

        # Create/Connect to database
        self.conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        # Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS tblplaque(
            id serial PRIMARY KEY,
            url text,
            owner_name VARCHAR(255),
            mailing_address text,
            ward VARCHAR(255),
            deeds_amount numeric(5, 2)
        )
        """)

    def process_item(self, item, spider):
        # Define insert statement
        self.cur.execute(""" insert into books (url, owner_name, mailing_address, ward, deeds_amount) values (%s,%s,%s,%s,%s)""", (
            item["url"],
            str(item["owner_name"]),
            str(item["mailing_address"]),
            str(item["ward"]),
            item["deeds_amount"]
        ))

        # Execute insert of data into database
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
