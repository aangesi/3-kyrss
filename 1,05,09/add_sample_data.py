import sqlite3
from tabulate import tabulate

conn = sqlite3.connect("game_platform.db")
cursor = conn.cursor()

# === Добавляем данные ===

players = [
    ("Alice", "2024-01-15"),
    ("Bob", "2023-11-03"),
    ("Charlie", "2024-06-10"),
    ("Diana", "2022-08-25"),
    ("Eve", "2024-02-29")
]
cursor.executemany("INSERT INTO Players (Name, RegistrationDate) VALUES (?, ?);", players)

games = [
    ("Cyber Arena",),
    ("Space Fighters",),
    ("Mystic Quest",)
]
cursor.executemany("INSERT INTO Games (Title) VALUES (?);", games)

matches = [
    (1, "2025-01-01"),
    (1, "2025-01-03"),
    (2, "2025-01-04"),
    (3, "2025-01-05"),
    (2, "2025-01-06"),
    (1, "2025-01-07"),
    (3, "2025-01-08"),
    (1, "2025-01-09"),
    (2, "2025-01-10"),
    (3, "2025-01-11")
]
cursor.executemany("INSERT INTO Matches (GameID, MatchDate) VALUES (?, ?);", matches)

scores = [
    (1, 1, 10, 2, 1500, True),
    (2, 1, 8, 5, 1200, False),
    (3, 2, 12, 4, 1700, True),
    (1, 2, 7, 6, 1100, False),
    (4, 3, 15, 5, 1800, True),
    (5, 3, 10, 8, 1300, False),
    (2, 4, 20, 10, 2000, True),
    (3, 4, 5, 12, 900, False),
    (1, 5, 14, 4, 1600, True),
    (5, 5, 13, 9, 1400, False),
    (2, 6, 18, 3, 2100, True),
    (4, 6, 10, 10, 1200, False),
    (3, 7, 11, 7, 1500, True),
    (1, 7, 9, 11, 1000, False),
    (5, 8, 16, 6, 1900, True),
    (2, 8, 5, 9, 800, False),
    (4, 9, 7, 8, 1000, False),
    (1, 9, 12, 4, 1700, True),
    (3, 10, 8, 4, 1400, True),
    (5, 10, 6, 10, 700, False)
]
cursor.executemany("""
INSERT INTO PlayerScores (PlayerID, MatchID, Kills, Deaths, Score, IsWinner)
VALUES (?, ?, ?, ?, ?, ?);
""", scores)

conn.commit()

# === ЗАПРОСЫ С ТАБЛИЧНЫМ ВЫВОДОМ ===

def run_query(title, query, headers=None):
    print(f"\n🔹 {title}")
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        print("Нет данных.")
    else:
        print(tabulate(rows, headers=headers, tablefmt="grid"))

# 1. Игроки, зарегистрированные в 2024
run_query(
    "Игроки, зарегистрированные в 2024 году:",
    """
    SELECT PlayerID, Name, RegistrationDate
    FROM Players
    WHERE strftime('%Y', RegistrationDate) = '2024';
    """,
    headers=["ID", "Имя", "Дата регистрации"]
)

# 2. Средний балл игрока с ID = 1
run_query(
    "Средний балл игрока с ID = 1:",
    """
    SELECT AVG(Score) as AvgScore
    FROM PlayerScores
    WHERE PlayerID = 1;
    """,
    headers=["Средний балл"]
)

# 3. Топ-5 популярных игр
run_query(
    "Топ-5 популярных игр по числу матчей:",
    """
    SELECT Games.Title, COUNT(Matches.MatchID) AS MatchCount
    FROM Games
    JOIN Matches ON Games.GameID = Matches.GameID
    GROUP BY Games.GameID
    ORDER BY MatchCount DESC
    LIMIT 5;
    """,
    headers=["Игра", "Количество матчей"]
)

# 4. Игрок с лучшим K/D
run_query(
    "Игрок с лучшим средним K/D:",
    """
    SELECT Players.Name, ROUND(AVG(CAST(Kills AS FLOAT) / NULLIF(Deaths, 0)), 2) AS KD_Ratio
    FROM PlayerScores
    JOIN Players ON Players.PlayerID = PlayerScores.PlayerID
    GROUP BY PlayerScores.PlayerID
    ORDER BY KD_Ratio DESC
    LIMIT 1;
    """,
    headers=["Игрок", "Среднее K/D"]
)

# 5. Игроки, участвовавшие в 'Cyber Arena', но ни разу не победили
run_query(
    "Игроки, участвовавшие в 'Cyber Arena', но ни разу не побеждали:",
    """
    SELECT DISTINCT Players.Name
    FROM PlayerScores
    JOIN Matches ON Matches.MatchID = PlayerScores.MatchID
    JOIN Games ON Games.GameID = Matches.GameID
    JOIN Players ON Players.PlayerID = PlayerScores.PlayerID
    WHERE Games.Title = 'Cyber Arena'
    AND Players.PlayerID NOT IN (
        SELECT PlayerScores.PlayerID
        FROM PlayerScores
        JOIN Matches ON Matches.MatchID = PlayerScores.MatchID
        JOIN Games ON Games.GameID = Matches.GameID
        WHERE Games.Title = 'Cyber Arena' AND PlayerScores.IsWinner = 1
    );
    """,
    headers=["Имя игрока"]
)

# 6. Полная статистика по матчу ID = 2
run_query(
    "Полная статистика матча ID = 2:",
    """
    SELECT 
        Matches.MatchID,
        Games.Title,
        Players.Name,
        PlayerScores.Score,
        PlayerScores.Kills,
        PlayerScores.Deaths,
        ROUND(CAST(PlayerScores.Kills AS FLOAT) / NULLIF(PlayerScores.Deaths, 0), 2) AS KD_Ratio
    FROM PlayerScores
    JOIN Players ON Players.PlayerID = PlayerScores.PlayerID
    JOIN Matches ON Matches.MatchID = PlayerScores.MatchID
    JOIN Games ON Games.GameID = Matches.GameID
    WHERE Matches.MatchID = 2;
    """,
    headers=["Матч ID", "Игра", "Игрок", "Счёт", "Kills", "Deaths", "K/D"]
)

conn.close()
