# queries.py

TABLE_registered = """
    CREATE TABLE IF NOT EXISTS registered (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    age TEXT,
    gender TEXT,
    date_age TEXT,
    email TEXT,
    photo TEXT
    )
"""

INSERT_TABLE_registered = """
    INSERT INTO registered (fullname, age, gender, date_age, email, photo)
    VALUES (?, ?, ?, ?, ?, ?)
"""

CREATETABLE_store = """
    CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product TEXT,
    size TEXT,
    price TEXT,
    photo TEXT,
    productid TEXT
    )
"""

INSERT_store = """
    INSERT INTO store (name_product, size, price, photo, productid)
    VALUES (?, ?, ?, ?, ?)
"""

CREATETABLE_store_detail = """
    CREATE TABLE IF NOT EXISTS store_detail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT,
    info_product TEXT,
    category TEXT,
    infoproduct TEXT
    )
"""

INSERT_store_detail = """
    INSERT INTO store_detail (product_id, info_product, category, infoproduct)
    VALUES (?, ?, ?, ?)
"""


CREATETABLE_products = """
    CREATE TABLE IF NOT EXISTS store_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product TEXT,
    size TEXT,
    price TEXT,
    photo TEXT,
    productid TEXT
    )
"""

INSERT_products = """
    INSERT INTO store_new (name_product, size, price, photo, productid)
    VALUES (?, ?, ?, ?, ?)
"""

CREATETABLE_products_details = """
    CREATE TABLE IF NOT EXISTS products_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    productid TEXT,
    category TEXT,
    infoproduct TEXT
    )
"""

INSERT_products_details = """
    INSERT INTO products_details (productid, category, infoproduct)
    VALUES (?, ?, ?)
"""


ALTER_STORE = """
    ALTER TABLE store 
    ADD COLUMN productid TEXT;
"""

ALTER_STORE_DETAIL = """
    ALTER TABLE store_detail 
    ADD COLUMN category TEXT,
    ADD COLUMN infoproduct TEXT;
"""
