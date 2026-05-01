import os
import tempfile
from unittest.mock import patch

import pytest

from src.utils import get_amount_in_rub
from src.utils import read_json_file


@pytest.mark.parametrize(
    "file_path, data, expected_result",
    [
        (None, None, []),
        ("", None, []),
        ("wrong/path.json", None, []),
        ("temp.json", "", []),
        ("temp.json", """{"answer": 42 }""", []),
        ("temp.json", """Non JSON data, or error in JSON""", []),
        ("temp.json", """[ {"id": 0} , {"id": 2} ]""", [{"id": 0}, {"id": 2}]),
    ],
)
def test_read_json_file(file_path, data, expected_result):
    if file_path == "temp.json":
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_json = os.path.join(tmpdir, "temp.json")
            if data is not None:
                with open(temp_json, "w", encoding="utf-8") as f:
                    f.write(data)
            assert read_json_file(temp_json) == expected_result
    else:
        assert read_json_file(file_path) == expected_result


@patch("src.utils.convert_currency")
def test_get_amount_in_rub(mocked_convert_currency):
    transaction = {
        "operationAmount": {"amount": "10", "currency": {"code": "USD"}},
    }
    mocked_convert_currency.return_value = 749.93688
    assert get_amount_in_rub(transaction) == 749.93688
    mocked_convert_currency.assert_called_once_with(10.0, "USD")


@patch("src.utils.convert_currency")
def test_get_amount_in_rub_from_rub(mocked_convert_currency):

    transaction = {
        "operationAmount": {"amount": "749.93688", "currency": {"code": "RUB"}},
    }
    assert get_amount_in_rub(transaction) == 749.93688
    mocked_convert_currency.assert_not_called()

@patch("src.utils.convert_currency")
def test_get_amount_in_rub_err(mocked_convert_currency):
    transaction = {
        "operationAmount": {"amour": "10", "currency": {"code": "USD"}},
    }
    mocked_convert_currency.return_value = 749.93688
    with pytest.raises(KeyError, match="Ошибка: Формат транзакции отличается. 'amount'"):
        get_amount_in_rub(transaction)

    transaction = {
        "operationAmount": {"amount": "десять", "currency": {"code": "USD"}},
    }

    with pytest.raises(
        ValueError, match="Ошибка: Формат транзакции отличается. could not convert string to float: 'десять'"
    ):
        get_amount_in_rub(transaction)

    transaction = {
        "operationAmount": {"amount": "10", "currency": {"code": ["USD"]}},
    }
    with pytest.raises(TypeError, match="Ошибка: Формат транзакции отличается. code должен быть строкой."):
        get_amount_in_rub(transaction)
