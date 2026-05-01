import os
import tempfile

import pytest

from src.decorators import log


@log()
def example_value_error(*args, **kvargs):
    raise ValueError("Ошибка значения в тестовой функции")


@log()
def example_type_error(*args, **kvargs):
    raise TypeError("Ошибка типа в тестовой функции")


@log()
def example_foo(*args, **kvargs):
    return "Ok"


def test_log_value_error():
    with pytest.raises(ValueError, match="Ошибка значения в тестовой функции"):
        example_value_error(666)


def test_log_type_error():
    with pytest.raises(TypeError, match="Ошибка типа в тестовой функции"):
        example_type_error(999)


def test_log_console(capsys):
    example_foo()
    captured = capsys.readouterr()
    assert ("Start: example_foo." in captured.out) and ("example_foo : Ok. Inputs: (), {}\n" in captured.out)


def test_log_file():
    # Создаём контекст с временной папкой для проверки создания и записи в лог файл
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "tmp_log_dir", "tmp.log")

        @log(log_file)
        def example_foo2(*args, **kwargs):
            return "Ok"

        example_foo2(42, name="answer")

        # Проверяем существование файла
        assert os.path.exists(log_file), "Лог-файл не создан"

        # Читаем содержимое файла
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Проверяем содержимое
        assert "Start: example_foo2" in content
        assert "example_foo2 : Ok" in content
        assert "Inputs: (42,), {'name': 'answer'}" in content
