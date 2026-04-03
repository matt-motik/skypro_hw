def get_mask_card_number(card_number: int) -> str:
    """Маскирует номер карты.
    Args:
        card_number: Номер карты (целое число)
    Returns:
        Маскированный номер карты
    Example:
        >>> get_mask_card_number(1234567890123456)
        '1234 56** **** 3456'
    """
    if not 0 <= card_number <= 9999999999999999:
        raise ValueError("Ошибка: card_number должен принимать числовое значение от 0 до 9999999999999999.")

    str_card_number = f"{card_number:016d}"
    return f"{str_card_number[:4]} {str_card_number[4:6]}** **** {str_card_number[-4:]}"


def get_mask_account(account_number: int) -> str:
    """Маскирует номер счета.
    Args:
        account_number: Номер счета (целое число)
    Returns:
        Маскированный номер счета в формате **XXXX
    Example:
        >>> get_mask_account(12345678901234567890)
        '**7890'
    """

    if not 0 <= account_number <= 99999999999999999999:
        raise ValueError("Ошибка: account_number должен принимать числовое значение от 0 до 99999999999999999999.")

    str_account_number = f"{account_number:020d}"
    return f"**{str_account_number[-4:]}"
