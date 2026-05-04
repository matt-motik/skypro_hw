# Модуль: `utils.py`

*Сгенерировано: 2026-05-04 21:25:57*

---

<div id="read_json_file"></div>

## read_json_file

**Тип:** function

**Кратко:** Функция чтения JSON-файла.

### Полная документация

```python
Функция чтения JSON-файла.

Args:
    filename: Путь к JSON-файлу транзакций.

Returns:
    Список транзакций.
    Если JSON-файл пустой, содержит не-список или не найден, возвращается пустой список.

Example:

    >>> transactions = read_json_file("data/operations.json")
```

---

<div id="get_amount_in_rub"></div>

## get_amount_in_rub

**Тип:** function

**Кратко:** Функция конвертации валюты из USD и EUR в рубли.

### Полная документация

```python
Функция конвертации валюты из USD и EUR в рубли.

Args:
    transaction: словарь с данными о транзакции.

Returns:
    Возвращает сумму транзакции (ключ amount) в рублях, тип данных float.

Example:

    >>> transaction = {"operationAmount": {"amount": "10.0", "currency": {"code": "USD"}}}
    >>> print(get_amount_in_rub(transaction))
    ... 749.93688
```

---

