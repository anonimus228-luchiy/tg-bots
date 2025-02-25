import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3")
        self.cursor = self.connection.cursor()

    def sql_create_tables(self):
        if self.connection:
            print("Database connected successfully")

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS store 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_product VARCHAR(255),
            size VARCHAR(50),
            price DECIMAL(10, 2),
            photo TEXT,
            productid INTEGER)
        """)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS products_details 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            productid INTEGER,
            category VARCHAR(100),
            infoproduct TEXT)
        """)
        
        self.connection.commit()

    def sql_insert_store_products(self, name_product, size, price, photo, productid):
        self.cursor.execute(
            "INSERT INTO store (id, name_product, size, price, photo, productid) VALUES (?, ?, ?, ?, ?, ?)",
            (None, name_product, size, price, photo, productid)
        )
        self.connection.commit()

    def sql_insert_products_details(self, productid, category, infoproduct):
        self.cursor.execute(
            "INSERT INTO products_details (id, productid, category, infoproduct) VALUES (?, ?, ?, ?)",
            (None, productid, category, infoproduct)
        )
        self.connection.commit()