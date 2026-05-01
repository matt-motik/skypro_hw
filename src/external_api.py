"""Модуль для работы с внешними API."""

import os

from dotenv import load_dotenv
import requests
from requests import RequestException


def convert_currency(amount: float, from_currency: str, to_currency: str = "RUB") -> float:
    """Функция конвертации валюты.

    Args:
        amount: сумма в изначальной валюте
        from_currency: из какой валюты
        to_currency: в какую валюту (по умолчанию 'RUB')

    Returns:
        сумма в новой валюте

    Example:

        >>> print(convert_currency(10, "USD", "RUB"))
        ... 749.93688
    """
    load_dotenv()
    api_key = os.getenv("ERD_API_KEY")

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"

    payload: dict[str, str | dict | float | bool] = {}
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers, data=payload)
    except RequestException as err:
        raise RequestException(f"Ошибка запроса: {err}")

    match response.status_code:
        case 200:
            data = response.json()
            try:
                result = float(data["result"])
                return result
            except KeyError as err:
                raise RuntimeError("Ошибка: API изменил формат ответа: отсутствует поле 'result'") from err
        case 400:
            raise RuntimeError("Ошибка запроса на сервер конвертации валюты")
        case 401:
            raise RuntimeError("Ошибка авторизации на сервере конвертации валюты")
        case 404:
            raise RuntimeError("Нет такого адреса у конвертации валюты")
        case 429:
            raise RuntimeError("Слишком много запросов к серверу конвертации валюты")
        case _:
            if response.status_code >= 500:
                raise RuntimeError("Внутрення ошибка сервера конвертации валюты")
            else:
                raise RuntimeError(f"Ошибка конвертации валюты: статус {response.status_code}")
