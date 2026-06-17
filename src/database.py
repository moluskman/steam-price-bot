import sqlite3

conn = sqlite3.connect("data/bot.db")


def init_db():  # Database initialization and function pointing to database file
    conn = sqlite3.connect("data/bot.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tracked_games (
            app_id INTEGER PRIMARY KEY,
            name TEXT,
            original_price REAL
)""")
    conn.commit()
    conn.close()


def add_tracked_game(app_id: int, name: str, original_price: float) -> bool:
    """Inserts a game into the database. Returns True if successful, False if already tracked."""
    conn = sqlite3.connect("data/bot.db")
    cursor = conn.cursor()
    try:  # insert or ignore avoids crashing if the game was already added
        cursor.execute(
            """
            INSERT OR IGNORE INTO tracked_games (app_id, name, original_price)
            VALUES (?, ?, ?)
        """,
            (app_id, name, original_price),
        )
        success = (
            cursor.rowcount > 0
        )  # if row was changed it means new game was added, otherwise it was already tracked
        conn.commit()
        print(f"DEBUG: Inserted game. Rowcount: {cursor.rowcount}, Success: {success}")
        return success
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()


def remove_tracked_game(app_id: int) -> str | None:
    """
    Deletes a game from the tracking database using its App ID.
    Returns the game's name if removed, or None if it wasn't tracked.
    """
    conn = sqlite3.connect("data/bot.db")  # opens connection to sqlite file
    cursor = conn.cursor()

    # Checks if the game exists in the database and grabs the row if found
    cursor.execute("SELECT name FROM tracked_games WHERE app_id = ?", (app_id,))
    result = cursor.fetchone()  # fetches the first row of the query result

    if result:
        game_name = result[0]  # extracts the game name from the query result

        # deletes the game with the matching app id
        cursor.execute("DELETE FROM tracked_games WHERE app_id = ?", (app_id,))

        conn.commit()  # commits the changes to the database
        conn.close()  # closes the connection safely
        return game_name  # returns the name of the deleted game

    # If the game was not found in the database
    conn.close()  # closes the connection safely
    return None  # returns None to indicate no game was found


def get_watchlist():  # watchlist retrieval function
    """Returns a list of all tracked games in the database"""
    conn = sqlite3.connect("data/bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracked_games")
    games = cursor.fetchall()  # fetches all rows of the query result
    conn.close()
    return games
