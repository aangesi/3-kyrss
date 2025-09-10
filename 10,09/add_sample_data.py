import sqlite3

def add_sample_data():
    # Подключение к базе данных
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Добавление данных в таблицу Students (с расширением списка)
    students = [
        (1, 'Иван', 'Иванов'),
        (2, 'Петр', 'Петров'),
        (3, 'Ирина', 'Иванова'),
        (4, 'Мария', 'Сидорова'),
        (5, 'Инна', 'Ильина'),
        (6, 'Игорь', 'Иванов'),
        (7, 'Ольга', 'Иванова'),
        (8, 'Дмитрий', 'Дмитриев'),
        (9, 'Александр', 'Иванов'),
        (10, 'Елена', 'Иванова'),
        (11, 'Андрей', 'Петров'),
        (12, 'Екатерина', 'Сидорова'),
        (13, 'Виктор', 'Ильин'),
        (14, 'Наталья', 'Иванова')
    ]
    cursor.executemany('''
        INSERT OR REPLACE INTO Students (StudentID, FirstName, LastName) VALUES (?, ?, ?)
    ''', students)

    # Добавление данных в таблицу Courses
    courses = [
        (1, 'Математика'),
        (2, 'Физика'),
        (3, 'Информатика'),
        (4, 'Химия'),
        (5, 'Биология')
    ]
    cursor.executemany('''
        INSERT OR REPLACE INTO Courses (CourseID, CourseName) VALUES (?, ?)
    ''', courses)

    # Добавление данных в таблицу Enrollments
    enrollments = [
        (1, 1, 1),  # Иванов записан на Математику
        (2, 2, 2),  # Петров записан на Физику
        (3, 3, 3),  # Иванова записана на Информатику
        (4, 4, 1),  # Сидорова записана на Математику
        (5, 1, 2),  # Иванов записан на Физику
        (6, 3, 2),  # Иванова записана на Физику
        (7, 5, 4),  # Ильина записана на Химию
        (8, 6, 5),  # Иванов записан на Биологию
        (9, 7, 1),  # Иванова записана на Математику
        (10, 8, 3), # Дмитриев записан на Информатику
        (11, 9, 4), # Иванов записан на Химию
        (12, 10, 5),# Иванова записана на Биологию
        (13, 11, 3),# Петров записан на Информатику
        (14, 12, 1),# Сидорова записана на Математику
        (15, 13, 2),# Ильин записан на Физику
        (16, 14, 5) # Иванова записана на Биологию
    ]
    cursor.executemany('''
        INSERT OR REPLACE INTO Enrollments (EnrollmentID, StudentID, CourseID) VALUES (?, ?, ?)
    ''', enrollments)

    # Сохраняем изменения и закрываем соединение
    conn.commit()

    # Выполнение SQL-запроса с INNER JOIN
    query = '''
        SELECT Students.StudentID, Students.FirstName, Students.LastName, Courses.CourseName
        FROM Students
        INNER JOIN Enrollments ON Students.StudentID = Enrollments.StudentID
        INNER JOIN Courses ON Enrollments.CourseID = Courses.CourseID
        WHERE Students.LastName LIKE 'И%'
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    # Выводим результаты запроса
    print("Students whose last name starts with 'И':")
    for row in results:
        print(f"StudentID: {row[0]}, FirstName: {row[1]}, LastName: {row[2]}, CourseName: {row[3]}")

    # Закрываем соединение
    conn.close()

if __name__ == '__main__':
    add_sample_data()
