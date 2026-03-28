from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_number: str) -> str:
    """Функция принимает на вход строку информации о карте или счете. Возвращает замаскированную строку."""
    number_type, number = (account_card_number.rsplit(" ", 1))
    masked_number = number_type
    match number_type:
        case "Счет":
            masked_number = get_mask_account(int(number))
        case default:
            masked_number = get_mask_card_number(int(number))

    return f"{number_type} {masked_number}"


# print(mask_account_card("Visa Platinum 7000792289606361"))
# print(mask_account_card("Maestro 7000792289606361"))
# print(mask_account_card("Счет 73654108430135874305"))