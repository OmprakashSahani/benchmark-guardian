import sqlite3


DATABASE_NAME = "benchmark_guardian.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS benchmark_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baseline REAL NOT NULL,
            current REAL NOT NULL,
            change_percent REAL NOT NULL,
            regression BOOLEAN NOT NULL,
            severity TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()
