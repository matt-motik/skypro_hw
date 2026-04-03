def filter_by_state(operations: list, state: str = 'EXECUTED') -> list:
    """Функция принимает на вход список словарей с данными о банковских операциях и параметр state,
    возвращает новый список, содержащий только те словари, у которых ключ state содержит переданное в функцию значение.
    Параметр state функции имеет значение по умолчанию 'EXECUTED'
    """
    if not isinstance(operations, list):
        return []
    return [operation for operation in operations if operation.get('state') == state]


# test_data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#               {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#               {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#               {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

# print(filter_by_state(test_data, state='EXECUTED'))
# print(filter_by_state(test_data))
# print(filter_by_state(test_data, state='CANCELED'))
# print(filter_by_state(test_data, state=''))
# print(filter_by_state(test_data, state=None))
# test_data = []
# print(filter_by_state(test_data, state='EXECUTED'))
# test_data = [{}]
# print(filter_by_state(test_data, state='EXECUTED'))

def sort_by_date(operations: list, reverse: bool = True):
    """Функция принимает на вход список словарей и параметр порядка сортировки, возвращает новый список,
     в котором исходные словари отсортированы по дате.
     Параметр порядка сортировки функции имеет значение по умолчанию 'True'
     """
    if not isinstance(operations, list):
        return []
    return sorted(operations, key=lambda operation: operation.get('date',''), reverse=reverse)

# print(sort_by_date(test_data))
# print(sort_by_date(test_data, False))
# test_data = [{}]
# print(sort_by_date(test_data))
# test_data = []
# print(sort_by_date(test_data))
# test_data = None
# print(sort_by_date(test_data))