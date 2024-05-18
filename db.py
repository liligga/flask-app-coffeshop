from flask import g, current_app, Flask
import sqlite3
from products import products


def get_db():
    """Функция для подключения к базе данных"""
    db = getattr(g, '_database', None)
    if db is None:
        g._database = sqlite3.connect('db.sqlite')
        g._database.row_factory = sqlite3.Row
        db = g._database
    return db


def close_db(e=None):
    """Функция для закрытия подключения к базе данных"""
    db = g.pop('_database', None)
    if db is not None:
        db.close()


def init_db(app: Flask):
    """Инициализация базы данных"""
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                email TEXT,
                total_price FLOAT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price FLOAT,
                old_price FLOAT,
                image TEXT,
                description TEXT
            )
        """)
        for pr in products:
            db.execute("""
                       INSERT INTO products
                       (name, price, old_price, image, description) VALUES
                       (?, ?, ?, ?, ?) 
           """, (pr['name'], pr['price'], pr['old_price'], pr['image'], pr['description']))
        db.commit()
