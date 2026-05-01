"""Модуль реализующий декораторы."""

from datetime import datetime
from functools import wraps
import os
from typing import Any
from typing import Callable


def log(filename: str | None = None) -> Callable:
    """Декоратор для логирования вызовов функций.

    Args:
        filename: Путь к файлу лога. Если None - вывод в консоль.

    Returns:
        Декоратор функции.

    Example:
        @log()
        def my_func():
            pass

        @log(filename="logs/app.log")
        def another_func():
            pass
    """

    def decorator(func: Callable) -> Callable:
        """Декоратор для обёртки функции."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обёртка, выполняющая логирование."""
            result = None

            if filename:
                directory = os.path.dirname(filename)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)

                if not os.path.exists(filename):
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"# Лог-файл создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}\n")
                        f.write("-" * 50 + "\n")

            def __print_or_write(file_str: str | None, message_str: str) -> None:
                msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}. {message_str}"
                if file_str:
                    with open(file_str, "a", encoding="utf-8") as f:
                        f.write(msg + "\n")
                else:
                    print(msg)

            try:
                message = f"Start: {func.__name__}."
                __print_or_write(filename, message)

                result = func(*args, **kwargs)

                message = f"{func.__name__} : {result}. Inputs: {args}, {kwargs}"
                __print_or_write(filename, message)
            except Exception as err:
                message = f"{func.__name__} error: {err} Inputs: {args}, {kwargs}"
                __print_or_write(filename, message)
                raise

            return result

        return wrapper

    return decorator
