"""Модуль реализующий функции по работе с файлами транзакций."""

import csv
import logging
import os

import pandas as pd

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"logs/{__name__}.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_transactions_csv(filepath: str) -> list[dict]:
    """Функция для считывания финансовых операций из CSV.

    Args:
        filepath: Путь к CSV-файлу транзакций.

    Returns:
        Список транзакций.
        Если CSV-файл пустой или не найден, возвращается пустой список.

    Example:

        >>> transactions = get_transactions_csv("data/transactions.csv")
    """
    logger.debug(f"Проверка CSV-файла '{filepath}' на существование")
    if filepath:
        if os.path.exists(filepath):
            logger.debug(f"CSV-файл '{filepath}' существует")
            logger.debug(f"Открываем CSV-файл '{filepath}' на чтение")
            transactions = []
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    logger.debug("Читаем CSV-файл")
                    reader = csv.DictReader(f, delimiter=";")
                    for row in reader:
                        if not row or all(value in (None, "") for value in row.values()):
                            logger.warning("Обнаружена пустая строка, пропускаем")
                            continue
                        try:
                            row["id"] = int(row["id"]) if row["id"] else 0
                        except (ValueError, TypeError):
                            logger.warning(f"Не удалось преобразовать id: {row.get('id')}")
                            row["id"] = None
                        try:
                            row["amount"] = int(row["amount"]) if row["amount"] else 0
                        except (ValueError, TypeError):
                            logger.warning(f"Не удалось преобразовать amount: {row.get('amount')}")
                            row["amount"] = None
                        transactions.append(row)
                    logger.debug("Транзакции успешно прочитаны")
                    return transactions
            except Exception as err:
                logger.error(f"Не удалось прочитать данные из CSV-файла. Возвращаем []. {str(err)}", exc_info=True)
                return []
    logger.error("Неверный путь. Возвращаем []")
    return []


def get_transactions_excel(filepath: str) -> list[dict]:
    """Функция для считывания финансовых операций из Excel.

    Args:
        filepath: Путь к Excel-файлу транзакций.

    Returns:
        Список транзакций.
        Если Excel-файл пустой или не найден, возвращается пустой список.

    Example:

        >>> transactions = get_transactions_excel("data/transactions_excel.xlsx")
    """
    logger.debug(f"Проверка Excel-файла '{filepath}' на существование")
    if filepath:
        if os.path.exists(filepath):
            logger.debug(f"Excel-файл '{filepath}' существует")
            logger.debug(f"Открываем Excel-файл '{filepath}' на чтение")
            try:
                transactions_df = pd.read_excel(filepath)
                transactions_df = transactions_df.dropna(how="all").reset_index(drop=True)
                transactions_df = transactions_df.convert_dtypes()
                transactions = transactions_df.to_dict(orient="records")
                logger.debug("Транзакции успешно прочитаны")
                return transactions
            except Exception as err:
                logger.error(f"Не удалось прочитать данные из Excel-файла. Возвращаем []. {str(err)}", exc_info=True)
                return []
    logger.error("Неверный путь. Возвращаем []")
    return []
