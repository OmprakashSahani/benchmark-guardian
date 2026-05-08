from app.db.database import get_connection


def save_benchmark_run(result: dict) -> None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO benchmark_runs (
            baseline,
            current,
            change_percent,
            regression,
            severity
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            result["baseline"],
            result["current"],
            result["change_percent"],
            result["regression"],
            result["severity"],
        ),
    )

    connection.commit()
    connection.close()
