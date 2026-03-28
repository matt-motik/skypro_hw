from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_number: str) -> str:
    """Функция принимает на вход строку информации о карте или счете. Возвращает замаскированную строку."""
    number_type, number = account_card_number.rsplit(" ", 1)
    masked_number: str = ""
    match number_type.lower():
        case "счет":
            masked_number = get_mask_account(int(number))
        case _:
            masked_number = get_mask_card_number(int(number))

    return f"{number_type} {masked_number}"


# print(mask_account_card("Visa Platinum 7000792289606361"))
# print(mask_account_card("Maestro 7000792289606361"))
# print(mask_account_card("Счет 73654108430135874305"))


def get_date(date_string: str) -> str:
    """Функция принимает на вход на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")."""
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")


# print(get_date("2024-03-11T02:26:18.671407"))
