import json
import logging

logger = logging.getLogger(__name__)


def validate_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, ValueError) as e:
        logger.warning("не удалось прочитать конфигурацию: %s", e)
        return False

    if not isinstance(config, dict):
        logger.warning("корень должен быть объектом")
        return False

    host = config.get("host")
    if not isinstance(host, str) or not host.strip():
        logger.warning("host: нужна непустая строка")
        return False

    port = config.get("port")
    if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
        logger.warning("port: нужно целое число от 1 до 65535")
        return False

    timeout = config.get("timeout")
    if not _is_number(timeout) or not 1 <= timeout <= 300:
        logger.warning("timeout: нужно число от 1 до 300")
        return False

    if not isinstance(config.get("enabled"), bool):
        logger.warning("enabled: нужно true или false")
        return False

    return True


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)
