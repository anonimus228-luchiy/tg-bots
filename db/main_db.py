# main.py
from aiogram import executor
import logging
from handlers import commands, echo, quiz, store_fsm  # Убрали fsm_reg отсюда
from config import dp, Admins, bot
import buttons

async def on_startup(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text='Бот включен!', reply_markup=buttons.start)
        await create_tables()

async def on_shutdown(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text='Бот выключен!')

async def create_tables():
    import sqlite3
    db = sqlite3.connect('db/bot.sqlite3')
    cursor = db.cursor()
    
    # Таблица для регистрации пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registered (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        age TEXT,
        gender TEXT,
        date_age TEXT,
        email TEXT,
        photo TEXT
        )
    """)
    
    # Таблица для товаров
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_product TEXT,
        size TEXT,
        price TEXT,
        product_id TEXT UNIQUE,
        photo TEXT
        )
    """)
    
    # Таблица для дополнительной информации о товарах
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS store_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT,
        info_product TEXT,
        category TEXT,
        FOREIGN KEY (product_id) REFERENCES store(product_id)
        )
    """)
    
    db.commit()
    db.close()

async def sql_insert_registered(fullname, age, gender, date_age, email, photo):
    import sqlite3
    db = sqlite3.connect('db/bot.sqlite3')
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO registered (fullname, age, gender, date_age, email, photo)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (fullname, age, gender, date_age, email, photo))
    db.commit()
    db.close()

async def sql_insert_store(name_product, size, price, product_id, photo):
    import sqlite3
    db = sqlite3.connect('db/bot.sqlite3')
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO store (name_product, size, price, product_id, photo)
    VALUES (?, ?, ?, ?, ?)
    """, (name_product, size, price, product_id, photo))
    db.commit()
    db.close()

async def sql_insert_store_detail(product_id, info_product, category):
    import sqlite3
    db = sqlite3.connect('db/bot.sqlite3')
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO store_details (product_id, info_product, category)
    VALUES (?, ?, ?)
    """, (product_id, info_product, category))
    db.commit()
    db.close()