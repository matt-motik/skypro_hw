# Модуль: `generators.py`

*Сгенерировано: 2026-05-02 01:13:14*

---

<div id="filter_by_currency"></div>

## filter_by_currency

**Тип:** function

**Кратко:** Фильтрует транзакции по значению ключа 'currency'.

### Полная документация

```python
Фильтрует транзакции по значению ключа 'currency'.

Args:
    transactions: Список словарей с банковскими транзакциями
    currency: Значение currency для фильтрации (по умолчанию 'USD')

Returns:
    Генератор отфильтрованных транзакций

Example:
    >>> usd_transactions = filter_by_currency(transactions, "USD")
    >>> for _ in range(2):
    ...     print(next(usd_transactions)["id"])
    ...
    939719570
    142264268
```

---

<div id="transaction_descriptions"></div>

## transaction_descriptions

**Тип:** function

**Кратко:** Возвращает описание каждой операции по очереди.

### Полная документация

```python
Возвращает описание каждой операции по очереди.

Args:
    transactions: Список словарей с банковскими транзакциями

Returns:
    Генератор с описаниями транзакций

Example:
    >>> descriptions = transaction_descriptions(transactions)
    >>> for _ in range(5):
    ...     print(next(descriptions))
    ...
    Перевод организации
    Перевод со счета на счет
    Перевод со счета на счет
    Перевод с карты на карту
    Перевод организации
```

---

<div id="card_number_generator"></div>

## card_number_generator

**Тип:** function

**Кратко:** Генератор выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где Х — цифра номера карты.

### Полная документация

```python
Генератор выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где Х — цифра номера карты.

Args:
    start_num: Начальный номер генерации карт
    stop_num: Конечный номер генерации карт

Returns:
    Генератор номеров в диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999.

Example:
    >>> for card_number in card_number_generator(1, 5):
    ...     print(card_number)

    0000 0000 0000 0001
    0000 0000 0000 0002
    0000 0000 0000 0003
    0000 0000 0000 0004
    0000 0000 0000 0005
```

---

