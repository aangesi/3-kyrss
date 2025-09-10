import sqlite3

def create_database():
    # Подключение к базе данных (или создание новой)
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            StudentID INTEGER PRIMARY KEY,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Courses (
            CourseID INTEGER PRIMARY KEY,
            CourseName TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Enrollments (
            EnrollmentID INTEGER PRIMARY KEY,
            StudentID INTEGER,
            CourseID INTEGER,
            FOREIGN KEY (StudentID) REFERENCES Students (StudentID),
            FOREIGN KEY (CourseID) REFERENCES Courses (CourseID)
        )
    ''')

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Database and tables created successfully!")
