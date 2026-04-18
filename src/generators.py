"""Модуль реализующий генераторы для обработки данных."""

from typing import Iterator

ERROR_MSG_INVALID_TYPE = "Ошибка: transactions должен быть cписком словарей с банковскими операциями."
ERROR_MSG_INVALID_CURRENCY_TYPE = "Ошибка: currency должен строкой."


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



def card_number_generator() -> Iterator[dict]:
    pass


