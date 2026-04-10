import pytest

from src.widget import ERROR_MSG_INVALID_DATE_FORMAT
from src.widget import ERROR_MSG_INVALID_FORMAT
from src.widget import get_date
from src.widget import mask_account_card


@pytest.mark.parametrize(
    "n, expected_result",
    [
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("Mastercard 1234567890123456", "Mastercard 1234 56** **** 3456"),
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("V 1", "V 0000 00** **** 0001"),
        (" 1", " 0000 00** **** 0001"),
    ],
)
def test_mask_account_card_normal(n, expected_result):
    assert mask_account_card(n) == expected_result


def test_mask_account_wrong_type():
    with pytest.raises(TypeError) as exc_info:
        mask_account_card(12345678901234567890)
    assert str(exc_info.value) == ERROR_MSG_INVALID_FORMAT


@pytest.mark.parametrize(
    "n",
    [
        "Visa Platinum 1234-5678-9012-3456",
        # "Visa Platinum 1234 5678 9012 3456",
        "Mastercard ",
        "Счет счёт",
    ],
)
def test_mask_account_wrong_format(n):
    with pytest.raises(TypeError) as exc_info:
        mask_account_card(n)
    assert str(exc_info.value) == ERROR_MSG_INVALID_FORMAT


def test_mask_account_empty_str():
    with pytest.raises(ValueError) as exc_info:
        mask_account_card("")
    assert str(exc_info.value) == ERROR_MSG_INVALID_FORMAT


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2021-04-12T02:26:18", "12.04.2021"),
        ("2022-05-13T02:26", "13.05.2022"),
        ("1983-08-31", "31.08.1983"),
    ],
)
def test_get_date_correct(date_str, expected):
    assert get_date(date_str) == expected


@pytest.mark.parametrize(
    "date_str",
    [
        "2024.03.11T02:26:18.671407",
        "2021/04/12T02:26:18",
        "12-25-2002",
        "date" "",
    ],
)
def test_get_date_wrong_format(date_str):
    with pytest.raises(ValueError) as exc_info:
        get_date(date_str)
    assert str(exc_info.value) == ERROR_MSG_INVALID_DATE_FORMAT


def test_get_date_wrong_type():
    with pytest.raises(TypeError) as exc_info:
        get_date(12323534)
    assert str(exc_info.value) == ERROR_MSG_INVALID_DATE_FORMAT
