from unittest.mock import patch

import pytest
from requests import RequestException

from src.external_api import convert_currency


@patch("src.external_api.requests.get")
def test_convert_currency(mocked_get):
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = {"result": 749.93688}
    assert convert_currency(10, "USD") == 749.93688


@patch("src.external_api.requests.get")
def test_convert_currency_err(mocked_get):
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = {"res": 749.93688}
    with pytest.raises(RuntimeError, match="Ошибка: API изменил формат ответа: отсутствует поле 'result'"):
        convert_currency(10, "USD")

    mocked_get.return_value.status_code = 400
    with pytest.raises(RuntimeError, match="Ошибка запроса на сервер конвертации валюты"):
        convert_currency(10, "USD")

    mocked_get.return_value.status_code = 401
    with pytest.raises(RuntimeError, match="Ошибка авторизации на сервере конвертации валюты"):
        convert_currency(10, "USD")

    mocked_get.return_value.status_code = 404
    with pytest.raises(RuntimeError, match="Нет такого адреса у конвертации валюты"):
        convert_currency(10, "USD")

    mocked_get.return_value.status_code = 429
    with pytest.raises(RuntimeError, match="Слишком много запросов к серверу конвертации валюты"):
        convert_currency(10, "USD")

    mocked_get.return_value.status_code = 500
    with pytest.raises(RuntimeError, match="Внутрення ошибка сервера конвертации валюты"):
        convert_currency(10, "USD")

    mocked_get.return_value.status_code = 418
    with pytest.raises(RuntimeError, match="Ошибка конвертации валюты: статус 418"):
        convert_currency(10, "USD")

    mocked_get.side_effect = RequestException("Connection failed")
    with pytest.raises(RequestException, match="Ошибка запроса: Connection failed"):
        convert_currency(10, "USD")
