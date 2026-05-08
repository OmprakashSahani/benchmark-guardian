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


def get_benchmark_runs() -> list[dict]:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            baseline,
            current,
            change_percent,
            regression,
            severity
        FROM benchmark_runs
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:
        results.append(
            {
                "id": row[0],
                "baseline": row[1],
                "current": row[2],
                "change_percent": row[3],
                "regression": bool(row[4]),
                "severity": row[5],
            }
        )

    return results
