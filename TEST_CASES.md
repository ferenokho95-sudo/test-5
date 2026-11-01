# Тест-кейсы для validate_config

Эталон: `{"host": "localhost", "port": 8080, "timeout": 30, "enabled": true}`.
В каждом кейсе меняется только указанное поле. `+` - конфигурация принята, `-` - отвергнута.

| № | Что проверяем | Данные | Тест | Ожидание |
|---|---------------|--------|------|----------|
| 1 | Эталонный файл | как в задании | `test_valid_file` | + |
| 2 | `port`, границы | `1`, `65535` | `test_valid_values` | + |
| 3 | `timeout`, границы и дробное | `1`, `300`, `1.5` | `test_valid_values` | + |
| 4 | `enabled` = false | `false` | `test_valid_values` | + |
| 5 | Лишнее поле | `"extra": "value"` | `test_valid_values` | + |
| 6 | `host` пустой | `""`, `"   "` | `test_invalid_host` | - |
| 7 | `host` не строка | `123`, `null` | `test_invalid_host` | - |
| 8 | `port` вне диапазона | `0`, `65536`, `-1` | `test_invalid_port` | - |
| 9 | `port` не целый | `8080.5`, `8080.0` | `test_invalid_port` | - |
| 10 | `port` другой тип | `"8080"`, `true`, `null` | `test_invalid_port` | - |
| 11 | `timeout` вне диапазона | `0`, `301` | `test_invalid_timeout` | - |
| 12 | `timeout` другой тип | `"30"`, `true`, `null` | `test_invalid_timeout` | - |
| 13 | `timeout` = NaN | `NaN` | `test_invalid_timeout` | - |
| 14 | `enabled` не bool | `"true"`, `1`, `null` | `test_invalid_enabled` | - |
| 15 | Нет одного из полей | по очереди все четыре | `test_missing_field` | - |
| 16 | Корень не объект | `[]`, `42`, `null` | `test_wrong_root` | - |
| 17 | Битый JSON | пустой файл, незакрытая скобка, запятая перед `}` | `test_broken_json` | - |
| 18 | Файла нет | несуществующий путь | `test_missing_file` | - |
| 19 | Вместо файла каталог | путь к каталогу | `test_directory_instead_of_file` | - |
| 20 | Не UTF-8 | байты `\xff\xfe` | `test_not_utf8` | - |
| 21 | Причина отказа в логе | `host=""`, `port=0`, `timeout=301` | `test_reason_is_logged` | в логе есть имя поля |

Не автоматизировано: файл без прав на чтение (под root не воспроизводится).
