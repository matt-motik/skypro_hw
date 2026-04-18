"""Модуль реализующий генераторы для обработки данных."""

from typing import Iterator

ERROR_MSG_INVALID_TYPE = "Ошибка: transactions должен быть cписком словарей с банковскими операциями."
ERROR_MSG_INVALID_CURRENCY_TYPE = "Ошибка: currency должен строкой."
ERROR_MSG_INVALID_START_TYPE = "Ошибка: start_num должен int."
ERROR_MSG_INVALID_STOP_TYPE = "Ошибка: stop_num должен int."
ERROR_MSG_INVALID_START_STOP_VALUE = "Ошибка: 1 <= start_num <= stop_num <= 9999999999999999"


def filter_by_currency(transactions: list[dict], currency: str = "USD") -> Iterator[dict]:
    """Фильтрует транзакции по значению ключа 'currency'.

    Args:
        transactions: Список словарей с банковскими транзакциями
        currency: Значение currency для фильтрации (по умолчанию 'USD')

    Returns:
        Генератор отфильтрованных транзакций

    Example:
        >>> usd_transactions = filter_by_currency(transactions, "USD")
        >>> for _ in range(2):
        ...     print(next(usd_transactions))
    """
    if not isinstance(transactions, list):
        raise TypeError(ERROR_MSG_INVALID_TYPE)
    if not isinstance(currency, str):
        raise TypeError(ERROR_MSG_INVALID_CURRENCY_TYPE)

    def check_currency(transaction: dict) -> bool:
        """Проверяет, соответствует ли валюта транзакции заданной."""
        try:
            return bool(transaction["operationAmount"]["currency"]["code"] == currency)
        except (KeyError, TypeError, AttributeError):
            # Пропускаем транзакции с некорректной структурой
            return False

    return filter(check_currency, transactions)


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """Возвращает описание каждой операции по очереди.

    Args:
        transactions: Список словарей с банковскими транзакциями

    Returns:
        Генератор с описаниями транзакций

    Example:
         >>> descriptions = transaction_descriptions(transactions)
         >>> for _ in range(5):
         ...     print(next(descriptions))
         >>> Перевод организации
    """
    if not isinstance(transactions, list):
        raise TypeError(ERROR_MSG_INVALID_TYPE)

    for transaction in transactions:
        if not isinstance(transaction, dict):
            continue
        yield transaction.get("description") or "Описание отсутствует"


def card_number_generator(start_num: int = 1, stop_num: int = 9999999999999999) -> Iterator[str]:
    """Генератор выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где Х — цифра номера карты.

    Args:
        start_num: Начальный номер генерации карт
        stop_num: Конечный номер генерации карт

    Returns:
        Генератор номеров в Диапазое от 0000 0000 0000 0001 до 9999 9999 9999 9999.

    Example:
        >>> for card_number in card_number_generator(1, 5):
        >>>     print(card_number)
        ...
        >>> 0000 0000 0000 0o001
        >>> 0000 0000 0000 0o002
        >>> 0000 0000 0000 0o003
        >>> 0000 0000 0000 0o004
        >>> 0000 0000 0000 0o005
    """
    if not isinstance(start_num, int):
        raise TypeError(ERROR_MSG_INVALID_START_TYPE)
    if not isinstance(stop_num, int):
        raise TypeError(ERROR_MSG_INVALID_STOP_TYPE)
    if not 1 <= start_num <= stop_num <= 9999999999999999:
        raise ValueError(ERROR_MSG_INVALID_START_STOP_VALUE)

    for num in range(start_num, stop_num + 1):
        num_str = str(num).zfill(16)
        number_str = f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:]}"
        yield number_str
