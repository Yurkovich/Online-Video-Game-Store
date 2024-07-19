import os
import sqlite3
from typing import Optional

from model.product import ProductModel

class Product:
    def __init__(self, db_name='database.db', folder_path=None):
        if folder_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            folder_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        
        self.db_path = os.path.join(folder_path, db_name)
        self.folder_path = folder_path

        self._create_db()

    def _create_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                image_url TEXT,
                genre TEXT,
                price INTEGER,
                discount INTEGER DEFAULT 0,
                quantity INTEGER DEFAULT 0,
                is_displayed BOOLEAN DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()

    def fetch_all_products(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()
        return products

    def add_product(self, product_name, image_url, genre, price, discount=0, quantity=0, is_displayed=True):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (product_name, image_url, genre, price, discount, quantity, is_displayed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (product_name, image_url, genre, price, discount, quantity, is_displayed))
        conn.commit()
        conn.close()

    def delete_product(self, product_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_product_by_id(product_id: int, db_path: str) -> Optional[ProductModel]:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        conn.close()

        if product:
            return ProductModel(
                id=product[0],
                product_name=product[1],
                image_url=product[2],
                genre=product[3],
                price=product[4],
                discount=product[5],
                quantity=product[6],
                is_displayed=bool(product[7])
            )
        return None

    @staticmethod
    def update_product(product_id, product_name=None, image_url=None, genre=None, price=None, discount=None, quantity=None, is_displayed=None, db_path=None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            folder_path = os.path.abspath(os.path.join(current_dir, os.pardir))
            db_path = os.path.join(folder_path, 'database.db')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        update_fields = []
        update_values = []

        if product_name is not None:
            update_fields.append('product_name = ?')
            update_values.append(product_name)
        if image_url is not None:
            update_fields.append('image_url = ?')
            update_values.append(image_url)
        if genre is not None:
            update_fields.append('genre = ?')
            update_values.append(genre)
        if price is not None:
            update_fields.append('price = ?')
            update_values.append(price)
        if discount is not None:
            update_fields.append('discount = ?')
            update_values.append(discount)
        if quantity is not None:
            update_fields.append('quantity = ?')
            update_values.append(quantity)
        if is_displayed is not None:
            update_fields.append('is_displayed = ?')
            update_values.append(is_displayed)

        update_values.append(product_id)

        update_query = 'UPDATE products SET ' + ', '.join(update_fields) + ' WHERE id = ?'
        cursor.execute(update_query, update_values)
        conn.commit()
        conn.close()

    def __str__(self):
        return f'Product(name={self.product_name}, genre={self.genre}, price={self.price}, quantity={self.quantity}, is_displayed={self.is_displayed})'

    def __repr__(self):
        return f'Product(product_name={self.product_name}, genre={self.genre}, price={self.price}, quantity={self.quantity}, is_displayed={self.is_displayed})'
    
pr_manager = Product()
# pr_manager.delete_product(10)
