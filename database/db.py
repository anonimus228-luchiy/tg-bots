import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Создаем таблицу категорий
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        
        # Создаем таблицу товаров
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT,
                FOREIGN KEY (category_id) REFERENCES categories (category_id)
            )
        """)
        
        # Создаем таблицу корзины
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES products (product_id),
                PRIMARY KEY (user_id, product_id)
            )
        """)
        
        # Создаем таблицу заказов
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                total_amount REAL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
    
    def add_category(self, name):
        self.cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        self.connection.commit()
    
    def add_product(self, category_id, name, description, price, image_url):
        self.cursor.execute(
            "INSERT INTO products (category_id, name, description, price, image_url) VALUES (?, ?, ?, ?, ?)",
            (category_id, name, description, price, image_url)
        )
        self.connection.commit()
    
    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories")
        return self.cursor.fetchall()
    
    def get_products_by_category(self, category_id):
        self.cursor.execute("SELECT * FROM products WHERE category_id = ?", (category_id,))
        return self.cursor.fetchall()
    
    def get_product(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        return self.cursor.fetchone()
    
    def add_to_cart(self, user_id, product_id):
        try:
            self.cursor.execute(
                "INSERT INTO cart (user_id, product_id) VALUES (?, ?)",
                (user_id, product_id)
            )
        except sqlite3.IntegrityError:
            self.cursor.execute(
                "UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND product_id = ?",
                (user_id, product_id)
            )
        self.connection.commit()
    
    def get_cart(self, user_id):
        self.cursor.execute("""
            SELECT p.*, c.quantity 
            FROM cart c 
            JOIN products p ON c.product_id = p.product_id 
            WHERE c.user_id = ?
        """, (user_id,))
        return self.cursor.fetchall()
    
    def clear_cart(self, user_id):
        self.cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        self.connection.commit()
    
    def create_order(self, user_id, total_amount):
        self.cursor.execute(
            "INSERT INTO orders (user_id, total_amount, status) VALUES (?, ?, 'new')",
            (user_id, total_amount)
        )
        self.connection.commit()
        return self.cursor.lastrowid