"""Модуль реализующий функции по работе с операциями."""

import json
import os.path

from src.decorators import log
from src.external_api import convert_currency


@log("logs/app.log")
def read_json_file(filename: str) -> list:
    """Функция чтения JSON-файла.

    Args:
        filename: Путь к JSON-файлу транзакций.

    Returns:
        Список транзакций.
        Если JSON-файл пустой, содержит не-список или не найден, возвращается пустой список.

    Example:

        >>> transactions = read_json_file("data/operations.json")
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


@log("logs/app.log")
def get_amount_in_rub(transaction: dict) -> float:
    """Функция конвертации валюты из USD и EUR в рубли.

    Args:
        transaction: словарь с данными о транзакции.

    Returns:
        Возвращает сумму транзакции (ключ amount) в рублях, тип данных float.

    Example:

        >>> transaction = {"operationAmount": {"amount": "10.0", "currency": {"code": "USD"}}}
        >>> print(get_amount_in_rub(transaction))
        ... 749.93688

    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        code = transaction["operationAmount"]["currency"]["code"]
        if not isinstance(code, str):
            raise TypeError("code должен быть строкой.")
    except Exception as err:
        raise type(err)(f"Ошибка: Формат транзакции отличается. {str(err)}") from err

    if code == "RUB":
        return amount
    else:
        return convert_currency(amount, code)
