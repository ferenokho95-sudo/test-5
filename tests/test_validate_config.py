import logging

import pytest

from config_validator import validate_config


def test_valid_file(valid_config_path):
    assert validate_config(valid_config_path) is True


@pytest.mark.parametrize(
    "changes",
    [
        {"port": 1},
        {"port": 65535},
        {"timeout": 1},
        {"timeout": 300},
        {"timeout": 1.5},
        {"enabled": False},
        {"extra": "value"},
    ],
)
def test_valid_values(changes, valid_config, write_config):
    valid_config.update(changes)

    assert validate_config(write_config(valid_config)) is True


@pytest.mark.parametrize("host", ["", "   ", 123, None])
def test_invalid_host(host, valid_config, write_config):
    valid_config["host"] = host

    assert validate_config(write_config(valid_config)) is False


@pytest.mark.parametrize("port", [0, 65536, -1, 8080.5, 8080.0, "8080", True, None])
def test_invalid_port(port, valid_config, write_config):
    valid_config["port"] = port

    assert validate_config(write_config(valid_config)) is False


@pytest.mark.parametrize("timeout", [0, 301, "30", True, None, float("nan")])
def test_invalid_timeout(timeout, valid_config, write_config):
    valid_config["timeout"] = timeout

    assert validate_config(write_config(valid_config)) is False


@pytest.mark.parametrize("enabled", ["true", 1, None])
def test_invalid_enabled(enabled, valid_config, write_config):
    valid_config["enabled"] = enabled

    assert validate_config(write_config(valid_config)) is False


@pytest.mark.parametrize("missing", ["host", "port", "timeout", "enabled"])
def test_missing_field(missing, valid_config, write_config):
    del valid_config[missing]

    assert validate_config(write_config(valid_config)) is False


@pytest.mark.parametrize("text", ["[]", "42", "null"])
def test_wrong_root(text, write_config):
    assert validate_config(write_config(text)) is False


@pytest.mark.parametrize(
    "text",
    ["", '{"host": "localhost", "port": 8080', '{"host": "h", "port": 80,}'],
)
def test_broken_json(text, write_config):
    assert validate_config(write_config(text)) is False


def test_missing_file(tmp_path):
    assert validate_config(tmp_path / "nope.json") is False


def test_directory_instead_of_file(tmp_path):
    assert validate_config(tmp_path) is False


def test_not_utf8(tmp_path):
    path = tmp_path / "config.json"
    path.write_bytes(b'{"host": "\xff\xfe"}')

    assert validate_config(path) is False


@pytest.mark.parametrize("field, value", [("host", ""), ("port", 0), ("timeout", 301)])
def test_reason_is_logged(field, value, valid_config, write_config, caplog):
    valid_config[field] = value

    with caplog.at_level(logging.WARNING):
        validate_config(write_config(valid_config))

    assert field in caplog.text
