import sqlite3

conn = sqlite3.connect("data/bot.db")


def init_db():  # Database initialization and function pointing to database file
    conn = sqlite3.connect("data/bot.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tracked_games (
    app_id INTEGER PRIMARY KEY,
    game_name TEXT,
    original_price REAL
)""")
    conn.commit()
    conn.close()
