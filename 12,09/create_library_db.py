import sqlite3

def create_database():
    # Создаем подключение к базе данных (если базы данных нет, она будет создана)
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Создаем таблицу employees
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_name TEXT NOT NULL,
        department TEXT NOT NULL
    )
    ''')

    # Создаем таблицу projects
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        employee_id INTEGER,
        FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
    )
    ''')

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database and tables created successfully.")
