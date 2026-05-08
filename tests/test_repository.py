from app.db.database import initialize_database
from app.repositories.benchmark_repository import (
    get_benchmark_runs,
    save_benchmark_run,
)


def test_save_and_get_benchmark_runs():
    initialize_database()

    result = {
        "baseline": 100.0,
        "current": 110.0,
        "change_percent": 10.0,
        "regression": True,
        "severity": "medium",
    }

    save_benchmark_run(result)

    runs = get_benchmark_runs()

    assert len(runs) > 0
    assert runs[0]["baseline"] == 100.0
    assert runs[0]["current"] == 110.0
    assert runs[0]["change_percent"] == 10.0
    assert runs[0]["regression"] is True
    assert runs[0]["severity"] == "medium"
