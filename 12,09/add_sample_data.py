import sqlite3

def add_sample_data():
    # Создаем подключение к базе данных
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Добавляем данные в таблицу employees
    employees = [
        ('Alice', 'IT'),
        ('Bob', 'HR'),
        ('Charlie', 'Finance'),
        ('David', 'IT')
    ]
    cursor.executemany('INSERT INTO employees (employee_name, department) VALUES (?, ?)', employees)

    # Добавляем данные в таблицу projects
    projects = [
        ('Project Alpha', 1),  # Alice работает на Project Alpha
        ('Project Beta', 2),   # Bob работает на Project Beta
        ('Project Gamma', 1)   # Alice работает на Project Gamma
    ]
    cursor.executemany('INSERT INTO projects (project_name, employee_id) VALUES (?, ?)', projects)

    # Сохраняем изменения
    conn.commit()

    # Выполняем SQL-запросы с OUTER JOIN

    # 1. Показать всех сотрудников и проекты, в которых они участвуют (LEFT OUTER JOIN)
    print("1. Все сотрудники и проекты, в которых они участвуют:")
    cursor.execute('''
    SELECT employees.employee_name, projects.project_name
    FROM employees
    LEFT OUTER JOIN projects ON employees.employee_id = projects.employee_id
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # 2. Показать все проекты и сотрудников, которые над ними работают (RIGHT OUTER JOIN)
    print("\n2. Все проекты и сотрудники, которые над ними работают:")
    cursor.execute('''
    SELECT projects.project_name, employees.employee_name
    FROM projects
    LEFT OUTER JOIN employees ON projects.employee_id = employees.employee_id
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # 3. Вывести список всех сотрудников, которые не работают ни над одним проектом
    print("\n3. Сотрудники, которые не работают ни над одним проектом:")
    cursor.execute('''
    SELECT employee_name
    FROM employees
    WHERE employee_id NOT IN (SELECT employee_id FROM projects)
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # 4. Показать всех сотрудников и все проекты (FULL OUTER JOIN)
    # В SQLite нет прямой поддержки FULL OUTER JOIN, но мы можем использовать UNION для достижения аналогичного результата.
    print("\n4. Все сотрудники и все проекты:")
    cursor.execute('''
    SELECT employees.employee_name, projects.project_name
    FROM employees
    LEFT OUTER JOIN projects ON employees.employee_id = projects.employee_id
    UNION
    SELECT employees.employee_name, projects.project_name
    FROM employees
    RIGHT OUTER JOIN projects ON employees.employee_id = projects.employee_id
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Закрываем соединение
    conn.close()

if __name__ == "__main__":
    add_sample_data()
    print("Sample data added and queries executed successfully.")
