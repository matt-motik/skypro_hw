# Модуль: `masks.py`

*Сгенерировано: 2026-04-18 22:48:19*

---

<div id="get_mask_card_number"></div>

## get_mask_card_number

**Тип:** function

**Кратко:** Маскирует номер карты.

### Полная документация

```python
Маскирует номер карты.

Args:
    card_number: Номер карты (целое число)

Returns:
    Маскированный номер карты

Example:
    >>> get_mask_card_number(1234567890123456)
    '1234 56** **** 3456'
```

---

<div id="get_mask_account"></div>

## get_mask_account

**Тип:** function

**Кратко:** Маскирует номер счета.

### Полная документация

```python
Маскирует номер счета.

Args:
    account_number: Номер счета (целое число)

Returns:
    Маскированный номер счета в формате **XXXX

Example:
    >>> get_mask_account(12345678901234567890)
    '**7890'
```

---

