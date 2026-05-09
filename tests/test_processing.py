import pytest

from src.processing import ERROR_MSG_INVALID_TYPE
from src.processing import filter_by_state
from src.processing import process_bank_operations
from src.processing import sort_by_date


@pytest.fixture()
def operations() -> list[dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 594226728, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture()
def operations_date_asc() -> list[dict]:
    return [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 594226728, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


@pytest.fixture()
def operations_date_desc() -> list[dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 594226728, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.fixture()
def operations_excluded() -> list[dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.fixture()
def operations_canceled() -> list[dict]:
    return [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 594226728, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture()
def operations_empty() -> list[dict]:
    return []


@pytest.mark.parametrize(
    "state, expected_fixture",
    [
        (None, "operations_excluded"),
        ("EXECUTED", "operations_excluded"),
        ("CANCELED", "operations_canceled"),
        ("PENDING", "operations_empty"),
    ],
)
def test_filter_by_state_parametrized(operations, state, expected_fixture, request):
    expected = request.getfixturevalue(expected_fixture)

    if state is None:
        assert filter_by_state(operations) == expected
    else:
        assert filter_by_state(operations, state=state) == expected


def test_filter_by_state_empty_list():
    assert filter_by_state([]) == []


def test_filter_by_state_empty_dict():
    assert filter_by_state([{}]) == []


def test_filter_by_state_wrong_type():
    with pytest.raises(TypeError) as exc_info:
        assert filter_by_state(123)
    assert str(exc_info.value) == ERROR_MSG_INVALID_TYPE


def test_filter_by_state_wrong_type_dict():
    with pytest.raises(TypeError) as exc_info:
        assert filter_by_state([123, "123"])
    assert str(exc_info.value) == ERROR_MSG_INVALID_TYPE


def test_sort_by_date_excluded(operations, operations_date_desc):
    assert sort_by_date(operations) == operations_date_desc
    assert sort_by_date(operations, reverse=True) == operations_date_desc


def test_sort_by_date_canceled(operations, operations_date_asc):
    assert sort_by_date(operations, reverse=False) == operations_date_asc


def test_sort_by_date_empty_list():
    assert sort_by_date([]) == []


def test_sort_by_date_empty_dict():
    assert sort_by_date([{}]) == [{}]


def test_sort_by_date_wrong_type():
    with pytest.raises(TypeError) as exc_info:
        assert sort_by_date(123)
    assert str(exc_info.value) == ERROR_MSG_INVALID_TYPE


def test_sort_by_date_wrong_type_dict():
    with pytest.raises(TypeError) as exc_info:
        assert sort_by_date([123, "123"])
    assert str(exc_info.value) == ERROR_MSG_INVALID_TYPE


def test_sort_by_date_stable_sort(operations):
    same_date = [op for op in operations if op["date"] == "2018-09-12T21:27:25.241689"]
    assert len(same_date) == 2
    assert same_date[0]["id"] == 594226727
    assert same_date[1]["id"] == 594226728

    sorted_ops = sort_by_date(operations)
    same_date_in_sorted = [op for op in sorted_ops if op["date"] == "2018-09-12T21:27:25.241689"]

    assert same_date_in_sorted[0]["id"] == 594226727
    assert same_date_in_sorted[1]["id"] == 594226728


def test_process_bank_operations():
    data = [
        {"description": "Перевод организации"},
        {"description": "Оплата услуг"},
        {"description": "Перевод организации"},
        {"description": "Покупка"},
    ]
    categories = ["Перевод организации", "Оплата услуг", "Кредит"]

    result = process_bank_operations(data, categories)

    assert result == {"Перевод организации": 2, "Оплата услуг": 1, "Кредит": 0}
