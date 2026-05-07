import os
import tempfile
from unittest.mock import mock_open
from unittest.mock import patch

import pandas as pd
import pytest

from src.transactions_readers import get_transactions_csv
from src.transactions_readers import get_transactions_excel


@pytest.mark.parametrize(
    "file_path, data, expected_result",
    [
        (None, None, []),
        ("", None, []),
        ("wrong/path.csv", None, []),
        ("temp.csv", "", []),
        ("temp.csv", """id;state;date;amount;currency_name;currency_code;from;to;description""", []),
        ("temp.csv", """Non csv data, or error in csv""", []),
    ],
)
def test_get_transactions_csv(file_path, data, expected_result):
    if file_path == "temp.csv":
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_csv = os.path.join(tmpdir, "temp.csv")
            if data is not None:
                with open(temp_csv, "w", encoding="utf-8") as f:
                    f.write(data)
            assert get_transactions_csv(temp_csv) == expected_result
    else:
        assert get_transactions_csv(file_path) == expected_result


@patch("os.path.exists")
def test_get_transactions_csv_with_mock_open(mock_exists):
    mock_exists.return_value = True
    mock_data = """id;amount
;

650703;16210"""

    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        result = get_transactions_csv("test.csv")

        assert result[0]["id"] == 650703
        assert result[0]["amount"] == 16210
        mock_file.assert_called_once_with("test.csv", "r", encoding="utf-8")


@patch("os.path.exists")
def test_get_transactions_csv_with_wrong_id_amount(mock_exists):
    mock_exists.return_value = True
    mock_data = "id;amount\nasd;fgb"

    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        result = get_transactions_csv("test.csv")

        assert result[0]["id"] is None
        assert result[0]["amount"] is None
        mock_file.assert_called_once_with("test.csv", "r", encoding="utf-8")


@patch("os.path.exists")
def test_get_transactions_csv_with_wrong_cant_read(mock_exists):
    mock_exists.return_value = True

    mock_file = mock_open()
    mock_file.side_effect = RuntimeError("Ошибка при чтении файла")

    with patch("builtins.open", mock_file):
        result = get_transactions_csv("test.csv")
        assert result == []
        mock_file.assert_called_once_with("test.csv", "r", encoding="utf-8")


@patch("pandas.read_excel")
@patch("os.path.exists")
def test_get_transactions_excel_with_read_error(mock_exists, mock_read_excel):
    mock_exists.return_value = True
    mock_read_excel.side_effect = RuntimeError("Ошибка при чтении файла")

    result = get_transactions_excel("test.xlsx")

    assert result == []
    mock_read_excel.assert_called_once_with("test.xlsx")


@pytest.mark.parametrize(
    "file_path, expected_result",
    [
        (None, []),
        ("", []),
        ("wrong/path.csv", []),
    ],
)
def test_get_transactions_excel_no_filepath(file_path, expected_result):
    assert get_transactions_excel(file_path) == expected_result


@patch("os.path.exists")
def test_get_transactions_excel(
    mock_exists,
):
    mock_exists.return_value = True
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test.xlsx")

        data = pd.DataFrame({"id": [1, 2, 3], "amount": [100, 200, 300], "currency_name": ["RUB", "RUB", "RUB"]})
        data.to_excel(file_path, index=False)

        result = get_transactions_excel(file_path)
        assert result[0]["id"] == 1
        assert result[0]["amount"] == 100
        assert result[0]["currency_name"] == "RUB"
        assert result[1]["id"] == 2
        assert result[1]["amount"] == 200
        assert result[1]["currency_name"] == "RUB"
        assert result[2]["id"] == 3
        assert result[2]["amount"] == 300
        assert result[2]["currency_name"] == "RUB"
