from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_number: str) -> str:
    """Маскирует номер карты или счета в строке.
    Args:
        account_card_number: Строка, содержащая тип и номер карты/счета
                             (например, "Visa Platinum 1234567890123456" или "Счет 12345678901234567890")
    Returns:
        Замаскированная строка с скрытым номером
    Example:
        >>>mask_account_card("Visa Platinum 1234567890123456")
        'Visa Platinum 1234 56** **** 3456'
        >>>mask_account_card("Счет 12345678901234567890")
        'Счет **7890'
    """
    number_type, number = account_card_number.rsplit(" ", 1)
    masked_number: str = ""
    match number_type.lower():
        case "счет":
            masked_number = get_mask_account(int(number))
        case _:
            masked_number = get_mask_card_number(int(number))
    return f"{number_type} {masked_number}"


def get_date(date_string: str) -> str:
    """Преобразует дату из ISO формата в формат ДД.ММ.ГГГГ.
    Args:
        date_string: Строка с датой в формате "ГГГГ-ММ-ДДTчч:мм:сс.микросекунды"
                     (например, "2024-03-11T02:26:18.671407")
    Returns:
        Строка с датой в формате "ДД.ММ.ГГГГ"
    Example:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
        >>> get_date("2019-07-03T18:35:29.512364")
        '03.07.2019'
    """
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")
