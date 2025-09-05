import sqlite3

def add_sample_data():
    # Создаем подключение к базе данных (или создаем её, если не существует)
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    # Создаем таблицы
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )''')

    # Вставляем данные
    cursor.executemany(''' 
    INSERT OR IGNORE INTO customers (name, email) VALUES (?, ?)
    ''', [
        ('Иван Иванов', 'ivan@mail.com'),
        ('Петр Петров', 'petr@mail.com'),
        ('Мария Смирнова', 'maria@mail.com')
    ])

    cursor.executemany('''
    INSERT OR IGNORE INTO categories (name) VALUES (?)
    ''', [
        ('Электроника',),
        ('Одежда',),
        ('Продукты питания',)
    ])

    cursor.executemany('''
    INSERT OR IGNORE INTO products (name, price, category_id) VALUES (?, ?, ?)
    ''', [
        ('Телевизор', 30000, 1),
        ('Наушники', 5000, 1),
        ('Футболка', 1500, 2),
        ('Хлеб', 50, 3),
        ('Смартфон', 25000, 1)
    ])

    cursor.executemany('''
    INSERT OR IGNORE INTO orders (customer_id, order_date) VALUES (?, ?)
    ''', [
        (1, '2023-03-05'),
        (2, '2023-05-01'),
        (3, '2023-01-10'),
    ])

    cursor.executemany('''
    INSERT OR IGNORE INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)
    ''', [
        (1, 1, 1),
        (1, 3, 2),
        (2, 2, 1),
        (2, 4, 3),
        (3, 5, 1),
    ])

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_sample_data()
