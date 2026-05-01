"""Модуль реализующий функции по работе с операциями."""

import json
import os.path

from src.decorators import log


@log("logs/app.log")
def read_json_file(filename: str) -> list:
    """Функция чтения JSON-файла.

    Args:
        filename: Путь к JSON-файлу транзакций.

    Returns:
        Список транзакций.
        Если JSON-файл пустой, содержит не-список или не найден, возвращается пустой список.

    Example:
        >>>transactions = read_json_file("data/operations.json")
    """
    if filename:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    transactions = json.load(f)
                except json.JSONDecodeError:
                    print("Error: Invalid JSON data. Return []")
                    return []
                if isinstance(transactions, list):
                    return transactions
                else:
                    print("Error: Data isn't a list. Return []")
                    return []
    print("Error: Wrong file path. Return []")
    return []
