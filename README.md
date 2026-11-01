# Проверка конфигурационного JSON-файла

`validate_config(path) -> bool` проверяет файл вида
`{"host": "localhost", "port": 8080, "timeout": 30, "enabled": true}`.

Правила:

- `host` - непустая строка;
- `port` - целое число от 1 до 65535;
- `timeout` - число от 1 до 300 (дробное можно);
- `enabled` - `true` или `false`;
- файл должен существовать, быть в UTF-8, содержать корректный JSON с объектом в корне.

Причина отказа пишется в лог (`logging`, уровень WARNING).

## Запуск

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

Python 3.9+. В `tests/test_validate_config.py` 13 тестовых функций, 45 проверок с учётом параметризации. После прогона результаты тестов дополнительно записываются
в `reports/results.log` (хук `pytest_runtest_logreport` в `tests/conftest.py`).

## Структура

- `config_validator.py` - функция `validate_config`;
- `tests/` - тесты; `conftest.py` - фикстуры и хук; `data/valid_config.json` - эталон;
- `TEST_CASES.md` - тест-кейсы.

## Принятые решения

- `true`/`false` в `port` и `timeout` не считаются числами;
- `8080.0` для `port` не считается целым;
- `host` из одних пробелов считается пустым;
- лишние поля игнорируются (в требованиях они не запрещены).
