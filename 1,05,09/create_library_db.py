import sqlite3

conn = sqlite3.connect("game_platform.db")
cursor = conn.cursor()

# Удаляем таблицы, если уже есть
cursor.executescript("""
DROP TABLE IF EXISTS PlayerScores;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Games;
""")

# Создаём таблицы
cursor.execute("""
CREATE TABLE Players (
    PlayerID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    RegistrationDate DATE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE Games (
    GameID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE Matches (
    MatchID INTEGER PRIMARY KEY AUTOINCREMENT,
    GameID INTEGER,
    MatchDate DATE,
    FOREIGN KEY (GameID) REFERENCES Games(GameID)
);
""")

cursor.execute("""
CREATE TABLE PlayerScores (
    ScoreID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlayerID INTEGER,
    MatchID INTEGER,
    Kills INTEGER,
    Deaths INTEGER,
    Score INTEGER,
    IsWinner BOOLEAN,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID)
);
""")

print("База данных и таблицы успешно созданы.")
conn.commit()
conn.close()
