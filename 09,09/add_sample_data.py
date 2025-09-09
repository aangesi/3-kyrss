import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Добавление данных в таблицу Departments
cursor.execute('''
INSERT INTO Departments (DepartmentID, DepartmentName, ManagerID) VALUES
(1, 'HR', 101),
(2, 'IT', 102),
(3, 'Marketing', 103)
''')

# Добавление данных в таблицу Employees
cursor.execute('''
INSERT INTO Employees (EmployeeID, FirstName, LastName, DepartmentID) VALUES
(1, 'John', 'Doe', 1),
(2, 'Jane', 'Smith', 2),
(3, 'Alice', 'Johnson', NULL),  -- сотрудник без отдела
(4, 'Bob', 'Brown', 3)
''')

# SQL-запрос с INNER JOIN для получения списка сотрудников с названием их отдела
cursor.execute('''
SELECT Employees.EmployeeID, Employees.FirstName, Employees.LastName, Departments.DepartmentName
FROM Employees
INNER JOIN Departments ON Employees.DepartmentID = Departments.DepartmentID
''')

# Выводим результаты
results = cursor.fetchall()
print("Employees with Department Names:")
for row in results:
    print(row)

# Объяснение
# В случае, если сотрудник не привязан к отделу (например, EmployeeID = 3), то INNER JOIN
# не вернёт этого сотрудника, так как INNER JOIN исключает строки, где нет совпадений.
# Для того чтобы получить всех сотрудников, включая тех, у кого нет отдела, нужно использовать LEFT JOIN.

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
