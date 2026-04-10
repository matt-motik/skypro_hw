import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


@pytest.mark.parametrize(
    "n, expected_result",
    [
        (1234567890123456, "1234 56** **** 3456"),
        (0, "0000 00** **** 0000"),
        (9999999999999999, "9999 99** **** 9999"),
        (123.567, "0000 00** **** 0123"),
    ],
)
def test_get_mask_card_number_normal(n, expected_result):
    assert get_mask_card_number(n) == expected_result


def test_get_mask_card_number_below_zero():
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(-1)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == "Ошибка: card_number должен принимать числовое значение от 0 до 9999999999999999."


def test_get_mask_card_number_above_max():
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(10000000000000000)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == "Ошибка: card_number должен принимать числовое значение от 0 до 9999999999999999."


def test_get_mask_card_number_wrong_type():
    with pytest.raises(TypeError) as exc_info:
        get_mask_card_number("1234567890123456")
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == "Ошибка: card_number должен принимать числовое значение от 0 до 9999999999999999."


@pytest.mark.parametrize(
    "n, expected_result",
    [
        (12345678901234567890, "**7890"),
        (0, "**0000"),
        (99999999999999999999, "**9999"),
        (123.567, "**0123"),
    ],
)
def test_gget_mask_account_normal(n, expected_result):
    assert get_mask_account(n) == expected_result


def test_get_mask_account_below_zero():
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(-1)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert (
        str(exc_info.value)
        == "Ошибка: account_number должен принимать числовое значение от 0 до 99999999999999999999."
    )


def test_get_mask_account_above_max():
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(100000000000000000000)
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert (
        str(exc_info.value)
        == "Ошибка: account_number должен принимать числовое значение от 0 до 99999999999999999999."
    )


def test_get_mask_account_wrong_type():
    with pytest.raises(TypeError) as exc_info:
        get_mask_account("12345678901234567890")
    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert (
        str(exc_info.value)
        == "Ошибка: account_number должен принимать числовое значение от 0 до 99999999999999999999."
    )
