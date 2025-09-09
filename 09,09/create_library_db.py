import sqlite3

# Подключаемся к базе данных (если не существует, создаём)
conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Создание таблицы Employees
cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    EmployeeID INTEGER PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT,
    DepartmentID INTEGER,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
)
''')

# Создание таблицы Departments
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments (
    DepartmentID INTEGER PRIMARY KEY,
    DepartmentName TEXT,
    ManagerID INTEGER
)
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
