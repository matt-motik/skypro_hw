# Модуль: `transactions_readers.py`

*Сгенерировано: 2026-05-05 22:29:15*

---

<div id="get_transactions_csv"></div>

## get_transactions_csv

**Тип:** function

**Кратко:** Функция для считывания финансовых операций из CSV.

### Полная документация

```python
Функция для считывания финансовых операций из CSV.

Args:
    filepath: Путь к CSV-файлу транзакций.

Returns:
    Список транзакций.
    Если CSV-файл пустой или не найден, возвращается пустой список.

Example:

    >>> transactions = get_transactions_csv("data/transactions.csv")
```

---

<div id="get_transactions_excel"></div>

## get_transactions_excel

**Тип:** function

**Кратко:** Функция для считывания финансовых операций из Excel.

### Полная документация

```python
Функция для считывания финансовых операций из Excel.

Args:
    filepath: Путь к Excel-файлу транзакций.

Returns:
    Список транзакций.
    Если Excel-файл пустой или не найден, возвращается пустой список.

Example:

    >>> transactions = get_transactions_excel("data/transactions_excel.xlsx")
```

---

