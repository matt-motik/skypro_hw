"""Основной модуль."""

import logging
from typing import Callable
from typing import cast

from src.generators import filter_by_currency
from src.processing import filter_by_state
from src.processing import process_bank_search
from src.processing import sort_by_date
from src.transactions_readers import convert_to_operation
from src.transactions_readers import get_transactions_csv
from src.transactions_readers import get_transactions_excel
from src.utils import read_json_file
from src.widget import get_date
from src.widget import mask_account_card

# Объявление переменных
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"
UNDERLINE = "\033[4m"

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f"logs/{__name__}.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def print_message(text: str) -> None:
    """Печать сообщения. (Жёлтым)text."""
    print(f"{YELLOW}{text}{RESET}")


def print_program_message(text: str) -> None:
    """Печать сообщения. "Программа: text"."""
    print(f"{MAGENTA}Программа: {YELLOW}{text}{RESET}")


def input_int(
    message: str,
    min_value: int | None = None,
    max_value: int | None = None,
    invalid_error: str = "Значение должно быть целым числом",
    min_error: str | None = None,
    max_error: str | None = None,
) -> int:
    """Защищённый ввод целого числа."""
    while True:
        value = input(message).strip()
        try:
            result = int(value)
        except ValueError:
            print(invalid_error)
            continue

        if min_value is not None and result < min_value:
            print(min_error or f"Значение должно быть целым числом больше {min_value}")
            continue

        if max_value is not None and result > max_value:
            print(max_error or f"Значение должно быть целым числом меньше {min_value}")
            continue

        return result


def choose_source() -> tuple[Callable, str]:
    """Выбор источника данных."""
    sources = {
        1: {
            "text": "Получить информацию о транзакциях из JSON-файла",
            "func": read_json_file,
            "name": "JSON-файл",
            "file": "data/operations.json",
        },
        2: {
            "text": "Получить информацию о транзакциях из CSV-файла",
            "func": get_transactions_csv,
            "name": "CSV-файл",
            "file": "data/transactions.csv",
        },
        3: {
            "text": "Получить информацию о транзакциях из XLSX-файла",
            "func": get_transactions_excel,
            "name": "XLSX-файл",
            "file": "data/transactions_excel.xlsx",
        },
    }

    print_message("Выберите необходимый пункт меню.")
    for key, value in sources.items():
        print(f"{GREEN}{key}. {RESET}", end="")
        print_message(str(value["text"]))
    print()
    source = input_int(
        f"{BLUE}Пользователь: {RESET}",
        min_value=1,
        max_value=len(sources),
        invalid_error=f"{RED}Введите число от 1 до {len(sources)}{RESET}",
        min_error=f"{RED}Введите число от 1 до {len(sources)}{RESET}",
        max_error=f"{RED}Введите число от 1 до {len(sources)}{RESET}",
    )

    selected = sources[source]
    print()
    print_program_message(f"Для обработки выбран {selected['name']}.\n")
    func: Callable = cast(Callable, selected["func"])
    file_name: str = str(selected["file"])
    return func, file_name


def input_choice(
    message: str,
    options: list[str],
    invalid_error: str | None = None,
) -> str:
    """Защищённый ввод из списка."""
    options_display = ", ".join(options)

    while True:
        value = input(message).strip()

        if value.lower() in [o.lower() for o in options]:
            return value

        if invalid_error:
            # Подставляем value и options_display в кастомный шаблон
            error_msg = invalid_error.format(value=value, options=options_display)
        else:
            error_msg = f"'{value}' нет в списке. Выберите из: {options_display}"

        print(error_msg)


def choose_status(status_list: list[str]) -> str:
    """Выбирает статус для фильтрации."""
    print_program_message("Введите статус, по которому необходимо выполнить фильтрацию. ")
    print_message(f"Доступные для фильтровки статусы: {', '.join(status_list)}\n")

    selected = input_choice(
        f"{BLUE}Пользователь: {RESET}",
        status_list,
        invalid_error="Программа: Статус операции {value} недоступен.\nВведите одно из значений {options}",
    )

    return selected.upper()


def print_operation(operation: dict) -> None:
    """Красивая печать операций в требуемом виде."""
    dt = get_date(operation.get("date", ""))
    desc = operation.get("description", "")
    from_str = operation.get("from", "")
    to_str = operation.get("to", "")
    currency = operation.get("operationAmount", {}).get("currency") or {}
    cur_name = currency.get("name", "")
    amount = operation.get("operationAmount", {}).get("amount", 0)
    if amount:
        amount = float(amount)
    print(f"{GREEN}{dt} {YELLOW} {desc}{RESET}")
    try:
        from_str = mask_account_card(from_str)
    except Exception as err:
        from_str = ""
        logger.warning(f"Нет значения from_str: '{from_str}'. {str(err)}", exc_info=True)
    try:
        to_str = mask_account_card(to_str)
    except Exception as err:
        to_str = ""
        logger.warning(f"Нет значения to_str: '{to_str}'. {str(err)}", exc_info=True)

    if from_str == "":
        print(f"{BLUE}{to_str}{RESET}")
    else:
        print(f"{BLUE}{from_str}{YELLOW} -> {BLUE}{to_str}{RESET}")

    print(f"{YELLOW}Сумма: {CYAN}{amount:g}{YELLOW} {cur_name}{RESET}")


if __name__ == "__main__":
    logger.info("Программа запущена")
    print_program_message("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    source_func, file_name = choose_source()
    logger.info("Читаем транзакции / операции")
    operations = source_func(file_name)
    if source_func != read_json_file:
        logger.info("Приводим транзакции к структуре операций")
        operations = [convert_to_operation(operation) for operation in operations]

    statuses = sorted(list(set(operation["state"].upper() for operation in operations)))
    if len(statuses) > 0:
        state_filter = choose_status(statuses)
        logger.info(f"Фильтруем по статусу {state_filter.lower()}")
        operations = filter_by_state(operations, state_filter)
        print()
        print_program_message(f'Операции отфильтрованы по статусу "{state_filter.lower()}".')

    print()
    print_program_message("Программа: Отсортировать операции по дате? Да/Нет\n")
    need_sort_by_date = input_choice(f"{BLUE}Пользователь: {RESET}", ["Да", "Нет"]).lower() == "да"
    if need_sort_by_date:
        print()
        print_program_message("Программа: Отсортировать по возрастанию или по убыванию? по возрастанию/по убыванию\n")
        need_sort_by_desc = (
            input_choice(f"{BLUE}Пользователь: {RESET}", ["по возрастанию", "по убыванию"]).lower() == "по убыванию"
        )
        logger.info(f"Сортируем по {'убыванию' if need_sort_by_desc else 'возрастанию'} даты")
        operations = sort_by_date(operations, need_sort_by_desc)

    print()
    print_program_message("Выводить только рублевые транзакции? Да/Нет\n")
    need_rub_currency = input_choice(f"{BLUE}Пользователь: {RESET}", ["Да", "Нет"]).lower() == "да"
    if need_rub_currency:
        logger.info("Фильтруем по currency = 'RUB'")
        operations = list(filter_by_currency(operations, currency="RUB"))

    print()
    print_program_message("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n")
    need_search_by_descr = input_choice(f"{BLUE}Пользователь: {RESET}", ["Да", "Нет"]).lower() == "да"

    if need_search_by_descr:
        search_str = input("Введите описание: ").strip().lower()
        logger.info(f"Фильтруем по определенному слову в описании: {search_str.lower()}")
        operations = process_bank_search(operations, search=search_str)

    print()
    print_program_message("Распечатываю итоговый список транзакций...\n")
    if len(operations) > 0:
        print_program_message(f"\nВсего банковских операций в выборке: {len(operations)}\n")
        for op in operations:
            print_operation(op)
            print()
        logger.info(f"Всего напечатано банковских операций в выборке: {len(operations)}")
    else:
        print_program_message("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        logger.info("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    logger.info("Программа выполнена")
