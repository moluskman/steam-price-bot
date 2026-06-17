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


def remove_tracked_game(
    app_id: int,
) -> bool:  # function to delete a game form being watched
    """
    Deletes a game from the tracking database using its App ID. Returns True if a game was removed, False otherwise,
    """
    conn = sqlite3.connect("data/bot.db")  # opens connection to sqlite file
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tracked_games WHERE app_id = ?", (app_id,)
    )  # deletes the game with the matching app id
    rows_affected = (
        cursor.rowcount
    )  # checks how many rows were affected by the delete command
    conn.commit()  # commits the changes to the database
    conn.close()  # closes the connection to the database

    return (
        rows_affected > 0
    )  # returns true if a game was deleted, false if no game was found with that app id
