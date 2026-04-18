import pytest

from generators import ERROR_MSG_INVALID_TYPE
from generators import filter_by_currency


@pytest.fixture()
def transactions() -> list[dict]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


def test_filter_by_currency_usd(transactions):
    gen = filter_by_currency(transactions, "USD")
    assert next(gen) == transactions[0]
    assert next(gen) == transactions[1]
    assert next(gen) == transactions[3]


def test_filter_by_currency_rub(transactions):
    gen = filter_by_currency(transactions, "RUB")
    assert next(gen) == transactions[2]
    assert next(gen) == transactions[4]


def test_filter_by_currency_type_error():
    with pytest.raises(TypeError) as exc_info:
        assert filter_by_currency(123, "RUB")
    assert str(exc_info.value) == ERROR_MSG_INVALID_TYPE


def test_filter_by_currency_btc(transactions):
    gen = filter_by_currency(transactions, "BTC")
    with pytest.raises(StopIteration):
        assert next(gen)


def test_filter_by_currency_broken_transaction(transactions):
    bad_transactions = transactions.copy()
    bad_transactions.append({"id": 999, "operationAmount": "invalid"})
    bad_transactions.append("not a dict")
    bad_transactions.append(None)
    gen = filter_by_currency(transactions, "RUB")
    assert next(gen) == transactions[2]
    assert next(gen) == transactions[4]
