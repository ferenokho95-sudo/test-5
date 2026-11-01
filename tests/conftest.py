import copy
import json
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"
REPORTS_DIR = Path(__file__).parent.parent / "reports"


@pytest.fixture(scope="session")
def valid_config_path():
    return DATA_DIR / "valid_config.json"


@pytest.fixture
def valid_config(valid_config_path):
    """Свежая копия эталонной конфигурации - тест может её менять."""
    return json.loads(valid_config_path.read_text(encoding="utf-8"))


@pytest.fixture
def write_config(tmp_path):
    """write_config(data) сохраняет dict (или готовую строку) во временный файл."""

    def write(data):
        path = tmp_path / "config.json"
        text = data if isinstance(data, str) else json.dumps(data)
        path.write_text(text, encoding="utf-8")
        return path

    return write


def pytest_runtest_logreport(report):
    """Хук: дописывает результат каждого теста в reports/results.log."""
    if report.when != "call":
        return
    REPORTS_DIR.mkdir(exist_ok=True)
    with open(REPORTS_DIR / "results.log", "a", encoding="utf-8") as f:
        f.write(f"{report.outcome.upper():7} {report.nodeid}\n")
