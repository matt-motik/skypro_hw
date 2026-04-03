def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует операции по значению ключа 'state'.
    Args:
        operations: Список словарей с банковскими операциями
        state: Значение state для фильтрации (по умолчанию 'EXECUTED')
    Returns:
        Отфильтрованный список операций
    """
    if not isinstance(operations, list):
        return []
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует операции по дате.
    Args:
        operations: Список словарей с банковскими операциями
        reverse: Направление сортировки. True - от новых к старым, False - от старых к новым (по умолчанию True)
    Returns:
        Отсортированный список операций
    """
    if not isinstance(operations, list):
        return []
    return sorted(operations, key=lambda operation: operation.get("date", ""), reverse=reverse)
