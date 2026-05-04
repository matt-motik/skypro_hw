"""Модуль реализующий функции по работе с операциями."""

import json
import logging
import os.path

from src.external_api import convert_currency

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/utils.log", mode='w')
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


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
    logger.debug(f"Проверка JSON-файла filename '{filename}' на существование")
    if filename:
        if os.path.exists(filename):
            logger.debug(f"JSON-файла '{filename}' существует")
            logger.debug(f"Открываем JSON-файл '{filename}' на чтение")
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    logger.debug("Читаем JSON-файл'")
                    transactions = json.load(f)
                except json.JSONDecodeError as err:
                    logger.warning(f"Invalid JSON data. Return []. {str(err)}", exc_info=True)
                    return []
                if isinstance(transactions, list):
                    logger.debug("Транзакции успешно прочитаны'")
                    return transactions
                else:
                    logger.warning("Data isn't a list. Return [].")
                    return []
    logger.warning("Wrong file path. Return []")
    return []


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
        logger.debug(f"Проверка структуры транзакции '{transaction}' на существование полей 'amount' и 'code'")
        amount = float(transaction["operationAmount"]["amount"])
        code = transaction["operationAmount"]["currency"]["code"]
        if not isinstance(code, str):
            raise TypeError("code должен быть строкой.")
    except Exception as err:
        logger.error(f"Формат транзакции отличается. {str(err)}", exc_info=True)
        raise type(err)(f"Ошибка: Формат транзакции отличается. {str(err)}") from err

    if code == "RUB":
        logger.debug(f"Транзакция в RUB, 'amount = {amount}'")
        return amount
    else:
        try:
            logger.debug(f"Транзакция в {code}. Запрашиваем конверсию у внешнего сервиса'")
            result = convert_currency(amount, code)
            logger.debug(f"Конверсия в RUB успешна, 'amount = {result}'")
            return result
        except Exception as err:
            logger.error(f"Не удалось выполнить конверсию. {str(err)}", exc_info=True)
            raise
