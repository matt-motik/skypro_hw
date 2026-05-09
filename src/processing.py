"""Модуль для обработки данных банковских операций."""

from collections import Counter
import logging
import re

ERROR_MSG_INVALID_TYPE = "Operations должен быть cписком словарей с банковскими операциями."

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"logs/{__name__}.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует операции по значению ключа 'state'.

    Args:
        operations: Список словарей с банковскими операциями
        state: Значение state для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Отфильтрованный список операций
    """
    if not isinstance(operations, list) or not all(isinstance(item, dict) for item in operations):
        logger.error(ERROR_MSG_INVALID_TYPE)
        raise TypeError(ERROR_MSG_INVALID_TYPE)
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует операции по дате.

    Args:
        operations: Список словарей с банковскими операциями
        reverse: Направление сортировки. True - от новых к старым, False - от старых к новым (по умолчанию True)

    Returns:
        Отсортированный список операций
    """
    if not isinstance(operations, list) or not all(isinstance(item, dict) for item in operations):
        logger.error(ERROR_MSG_INVALID_TYPE)
        raise TypeError(ERROR_MSG_INVALID_TYPE)
    return sorted(operations, key=lambda operation: operation.get("date", ""), reverse=reverse)


def process_bank_search(operations: list[dict], search: str) -> list[dict]:
    """Функция поиска операций по описанию.

    Args:
        data: список словарей с данными о банковских операциях
        search: строка поиска

    Returns:
        список словарей, у которых в описании есть данная строка

    Example:

        >>> results = process_bank_search(data, search  )
        ... print(results)
    """
    if not isinstance(operations, list) or not all(isinstance(item, dict) for item in operations):
        logger.error(ERROR_MSG_INVALID_TYPE)
        raise TypeError(ERROR_MSG_INVALID_TYPE)

    results = []
    search = search.strip().lower()
    pattern = re.compile(search, flags=re.IGNORECASE)
    for op in operations:
        if pattern.search(op["description"]):
            results.append(op)
    return results


def process_bank_operations(operations: list[dict], categories: list) -> dict:
    """Функция для подсчета количества банковских операций определенного типа.

    Args:
        data: список словарей с данными о банковских операциях
        categories: список категорий операций

    Returns:
        словарь, в котором ключи — это названия категорий, а значения — это количество операций в каждой категории.
        Категории операций хранятся в поле description

    Example:

        >>> results = process_bank_operations(operations, categories)
        ... print(results)
    """
    if not isinstance(operations, list) or not all(isinstance(item, dict) for item in operations):
        logger.error(ERROR_MSG_INVALID_TYPE)
        raise TypeError(ERROR_MSG_INVALID_TYPE)

    counter = Counter(op.get("description", "") for op in operations)
    return {category: counter.get(category, 0) for category in categories}
