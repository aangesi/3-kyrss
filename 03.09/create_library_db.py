import sqlite3

# Подключаемся к базе данных (если её нет — создаётся)
conn = sqlite3.connect("online_library.db")
cursor = conn.cursor()

# Создание таблицы Users
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    registration_date DATE NOT NULL
);
""")

# Таблица Authors
cursor.execute("""
CREATE TABLE IF NOT EXISTS Authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_year INTEGER
);
""")

# Таблица Genres
cursor.execute("""
CREATE TABLE IF NOT EXISTS Genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
""")

# Таблица Books
cursor.execute("""
CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    publish_year INTEGER,
    author_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id),
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);
""")

# Таблица Reviews
cursor.execute("""
CREATE TABLE IF NOT EXISTS Reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    rating INTEGER CHECK (rating >= 1 AND rating <= 15),                                                                                                 
    comment TEXT,
    review_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
);
""")

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных 'online_library.db' успешно создана и таблицы добавлены.")