def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает на вход список словарей с данными о банковских операциях и параметр state,
    возвращает новый список, содержащий только те словари, у которых ключ state содержит переданное в функцию значение.
    Параметр state функции имеет значение по умолчанию 'EXECUTED'
    """
    if not isinstance(operations, list):
        return []
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """Функция принимает на вход список словарей и параметр порядка сортировки, возвращает новый список,
    в котором исходные словари отсортированы по дате.
    Параметр порядка сортировки функции имеет значение по умолчанию 'True'
    """
    if not isinstance(operations, list):
        return []
    return sorted(operations, key=lambda operation: operation.get("date", ""), reverse=reverse)
