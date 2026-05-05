"""Модуль для маскировки номеров карт и счетов."""

import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/masks.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


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
    logger.debug(f"Проверка card_number '{card_number}' на соответствие требованиям")
    if not isinstance(card_number, (int, float)):
        logger.error(f"card_number '{card_number}' должен принимать числовое значение от 0 до 9999999999999999.")
        raise TypeError("Ошибка: card_number должен принимать числовое значение от 0 до 9999999999999999.")
    if not 0 <= card_number <= 9999999999999999:
        logger.error(f"card_number '{card_number}' должен принимать числовое значение от 0 до 9999999999999999.")
        raise ValueError("Ошибка: card_number должен принимать числовое значение от 0 до 9999999999999999.")

    str_card_number = f"{int(card_number):016d}"
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
    logger.debug(f"Проверка account_number '{account_number}' на соответствие требованиям")
    if not isinstance(account_number, (int, float)):
        logger.error(
            f"card_number '{account_number}' должен принимать числовое значение от 0 до 99999999999999999999."
        )
        raise TypeError("Ошибка: account_number должен принимать числовое значение от 0 до 99999999999999999999.")
    if not 0 <= account_number <= 99999999999999999999:
        logger.error(
            f"account_number '{account_number}' должен принимать числовое значение от 0 до 99999999999999999999."
        )
        raise ValueError("Ошибка: account_number должен принимать числовое значение от 0 до 99999999999999999999.")

    str_account_number = f"{int(account_number):020d}"
    return f"**{str_account_number[-4:]}"
