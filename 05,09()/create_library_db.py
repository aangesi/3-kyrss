import sqlite3

def run_queries():
    # Создаем подключение к базе данных
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    # Запрос 1: Найти всех клиентов, которые сделали заказы после 2023-01-01.
    cursor.execute('''
    SELECT DISTINCT c.name, c.email
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_date > '2023-01-01'
    ''')
    print("Клиенты, сделавшие заказы после 2023-01-01:")
    for row in cursor.fetchall():
        print(row)

    # Запрос 2: Подсчитать, сколько товаров продано по каждой категории.
    cursor.execute('''
    SELECT cat.name, SUM(oi.quantity) AS total_quantity
    FROM categories cat
    JOIN products p ON cat.category_id = p.category_id
    JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY cat.name
    ''')
    print("\nТовары, проданные по категориям:")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")

    # Запрос 3: Найти топ-3 самых дорогих товаров в интернет-магазине.
    cursor.execute('''
    SELECT name, price
    FROM products
    ORDER BY price DESC
    LIMIT 3
    ''')
    print("\nТоп-3 самых дорогих товара:")
    for row in cursor.fetchall():
        print(f"{row[0]} - {row[1]} руб.")

    # Запрос 4: Вывести список заказов с общей суммой (price * quantity) для каждого заказа.
    cursor.execute('''
    SELECT o.order_id, SUM(p.price * oi.quantity) AS total_sum
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY o.order_id
    ''')
    print("\nЗаказы с общей суммой:")
    for row in cursor.fetchall():
        print(f"Заказ {row[0]}: {row[1]} руб.")

    # Запрос 5: Определить клиента, который потратил больше всего денег.
    cursor.execute('''
    SELECT c.name, SUM(p.price * oi.quantity) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY c.customer_id
    ORDER BY total_spent DESC
    LIMIT 1
    ''')
    print("\nКлиент, который потратил больше всего денег:")
    row = cursor.fetchone()
    print(f"{row[0]}: {row[1]} руб.")

    # Закрываем соединение
    conn.close()

if __name__ == "__main__":
    run_queries()
