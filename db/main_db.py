# main_db.py
import sqlite3
from db import queries

db = sqlite3.connect('db/db.sqlite')
cursor = db.cursor()

async def create_tables():
    if db:
        print('База данных подключена')
    cursor.execute(queries.TABLE_registered)
    cursor.execute(queries.CREATETABLE_store)
    cursor.execute(queries.CREATETABLE_store_detail)
    cursor.execute(queries.CREATETABLE_products)
    cursor.execute(queries.CREATETABLE_products_details)


async def sql_insert_registered(fullname, age, gender, date_age, email, photo):
    cursor.execute(queries.INSERT_TABLE_registered, (fullname, age, gender, date_age, email, photo))
    db.commit()


async def sql_insert_store(name_product, size, price, photo, product_id):
    cursor.execute(queries.INSERT_store,
                   (name_product, size, price, photo, product_id)
                   )
    db.commit()


async def sql_insert_store_detail(product_id, info_product, category):
    cursor.execute(queries.INSERT_store_detail,
                   (product_id, info_product, category))
    db.commit()


# Новые функции для новых таблиц
async def sql_insert_products(name_product, size, price, photo, productid):
    cursor.execute(queries.INSERT_products,
                   (name_product, size, price, photo, productid)
                   )
    db.commit()


async def sql_insert_products_details(productid, category, infoproduct):
    cursor.execute(queries.INSERT_products_details,
                   (productid, category, infoproduct))
    db.commit()


def get_db_connection():
    conn = sqlite3.connect('db/db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    select * from store s
    INNER JOIN store_detail sd on s.product_id = sd.product_id
    """).fetchall()
    conn.close()
    return products


def delete_products(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM store_detail WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()