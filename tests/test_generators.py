import pytest

from generators import ERROR_MSG_INVALID_TYPE, ERROR_MSG_INVALID_CURRENCY_TYPE
from generators import filter_by_currency
from generators import transaction_descriptions


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


def test_filter_by_currency_usd_default(transactions):
    gen = filter_by_currency(transactions)
    assert next(gen) == transactions[0]


def test_filter_by_currency_rub(transactions):
    gen = filter_by_currency(transactions, "RUB")
    assert next(gen) == transactions[2]
    assert next(gen) == transactions[4]


def test_filter_by_currency_type_error():
    with pytest.raises(TypeError) as exc_info:
        assert filter_by_currency(123, "RUB")
    assert str(exc_info.value) == ERROR_MSG_INVALID_TYPE

def test_filter_by_currency_currency_type_error(transactions):
    with pytest.raises(TypeError) as exc_info:
        assert filter_by_currency(transactions, 111)
    assert str(exc_info.value) == ERROR_MSG_INVALID_CURRENCY_TYPE

def test_filter_by_currency_btc(transactions):
    gen = filter_by_currency(transactions, "BTC")
    with pytest.raises(StopIteration):
        assert next(gen)


def test_filter_by_currency_missing_keys():
    """Транзакция без вложенных ключей"""
    bad_transactions = [
        {"id": 1},
        {"id": 2, "operationAmount": {}},
        {"id": 3, "operationAmount": {"currency": {}}},
    ]
    gen = filter_by_currency(bad_transactions, "USD")
    with pytest.raises(StopIteration):
        next(gen)


def test_transaction_descriptions(transactions):
    descriptions = transaction_descriptions(transactions)
    assert next(descriptions) == transactions[0]["description"]
    assert next(descriptions) == transactions[1]["description"]
    assert next(descriptions) == transactions[2]["description"]
    assert next(descriptions) == transactions[3]["description"]
    assert next(descriptions) == transactions[4]["description"]

    with pytest.raises(StopIteration):
        assert next(descriptions)


def test_transaction_descriptions_type_error():
    gen = transaction_descriptions(123)
    with pytest.raises(TypeError) as exc_info:
        next(gen)
    assert str(exc_info.value) == ERROR_MSG_INVALID_TYPE


@pytest.fixture()
def transactions_with_invalid_data() -> list[dict]:
    return [
        {"id": 1, "description": "Есть описание"},
        1243,
        {"id": 2},
        {"id": 3, "description": None},
    ]
def test_transaction_descriptions_missing_description(transactions_with_invalid_data):
    gen = transaction_descriptions(transactions_with_invalid_data)
    assert next(gen) == "Есть описание"
    assert next(gen) == "Описание отсутствует"
    assert next(gen) == "Описание отсутствует"
    with pytest.raises(StopIteration):
        next(gen)