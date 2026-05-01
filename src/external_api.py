import os

import requests
from dotenv import load_dotenv
from requests import RequestException, Response


def convert_currency(amount: float, from_currency: str, to_currency: str = "RUB") -> float:
    load_dotenv()
    api_key = os.getenv('ERD_API_KEY')

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"

    payload = {}
    headers = {
        "apikey": api_key
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except RequestException as err:
        raise RequestException(f"Ошибка запроса: {err}")
    # response =  Response()
    # response.status_code = 200
    # response._content = b'{"date": "2018-02-22", "historical": "", "info": {"rate": 148.972231, "timestamp": 1519328414}, "query": {"amount": 25, "from": "GBP", "to": "JPY"}, "results": 3724.305775, "success": true}'
    # print(f"Status: {response.status_code}")
    # print(f"Response: {response.text}")
    match response.status_code:
        case 200:
            data = response.json()
            try:
                result = data["result"]
                return result
            except KeyError:
                raise RuntimeError("Ошибка: API изменил формат ответа: отсутствует поле 'result'")
        case 400:
            raise RuntimeError(f"Ошибка запроса на сервер конвертации валюты")
        case 401:
            raise RuntimeError(f"Ошибка авторизации на сервере конвертации валюты")
        case 404:
            raise RuntimeError(f"Нет такого адреса у конвертации валюты")
        case 429:
            raise RuntimeError(f"Слишком много запросов к серверу конвертации валюты")
        case default:
            if response.status_code >= 500:
                raise RuntimeError(f"Внутрення ошибка сервера конвертации валюты")
            else:
                raise RuntimeError(f"Ошибка конвертации валюты: статус {response.status_code}")



# print (convert_currency(10, "USD"))