"""Модуль реализующий генераторы для обработки данных."""

from typing import Iterator

ERROR_MSG_INVALID_TYPE = "Ошибка: transactions должен быть cписком словарей с банковскими операциями."


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

    def check_currency(transaction: dict) -> bool:
        """Проверяет, соответствует ли валюта транзакции заданной."""
        try:
            return bool(transaction["operationAmount"]["currency"]["code"] == currency)
        except (KeyError, TypeError, AttributeError):
            # Пропускаем транзакции с некорректной структурой
            return False

    return filter(check_currency, transactions)


def transaction_descriptions(transactions: list[dict]) -> Iterator[dict]:
    pass


def card_number_generator() -> Iterator[dict]:
    pass
