from unittest.mock import patch

from main import choose_source
from main import choose_status
from main import input_choice
from main import input_int
from main import print_message
from main import print_operation
from main import print_program_message


def test_print_message(capsys):
    print_message("Hello World")
    captured = capsys.readouterr()
    assert "Hello World" in captured.out


def test_print_program_message(capsys):
    print_program_message("Test")
    captured = capsys.readouterr()
    assert "Программа:" in captured.out
    assert "Test" in captured.out


def test_input_int_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "42")
    result = input_int("Enter number: ")
    assert result == 42


def test_input_int_with_min_max_value(monkeypatch, capsys):
    inputs = iter(["0", "5", "aa", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = input_int(
        "Enter: ",
        min_value=1,
        max_value=3,
        invalid_error="Не число!",
        min_error="Слишком мало!",
        max_error="Слишком много!",
    )
    assert result == 2
    captured = capsys.readouterr()
    assert "Не число!" in captured.out
    assert "Слишком мало!" in captured.out
    assert "Слишком много!" in captured.out


def test_input_choice_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "да")
    result = input_choice("Подтверждаете? Да/Нет", ["да", "нет"])
    assert result == "да"


def test_input_choice_custom_error_message(monkeypatch, capsys):
    inputs = iter(["не знаю", "ytn", "нет"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = input_choice(
        "Подтверждаете? Да/Нет",
        ["да", "нет"],
        invalid_error="Ошибка! '{value}' недопустимый ответ. Доступно: {options}",
    )
    assert result == "нет"
    captured = capsys.readouterr()
    assert "Ошибка! 'не знаю' недопустимый ответ. Доступно: да, нет" in captured.out
    assert captured.out.count("недопустимый ответ. Доступно: да, нет") == 2


def test_input_choice_multiple_invalid(monkeypatch, capsys):
    inputs = iter(["не знаю", "ytn", "нет"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = input_choice(
        "Подтверждаете? Да/Нет",
        ["да", "нет"],
    )
    assert result == "нет"
    captured = capsys.readouterr()
    assert captured.out.count("нет в списке") == 2


def test_choose_status_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "EXECUTED")
    result = choose_status(["EXECUTED", "CANCELED", "PENDING"])
    assert result == "EXECUTED"


def test_choose_status_invalid_then_valid(monkeypatch, capsys):
    inputs = iter(["test", "test", "CANCELED"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = choose_status(["EXECUTED", "CANCELED", "PENDING"])
    assert result == "CANCELED"
    captured = capsys.readouterr()
    assert "Статус операции test недоступен" in captured.out
    assert captured.out.count("недоступен") == 2


def test_print_operation_with_from_and_to(capsys):
    operation = {
        "date": "2024-03-11T02:26:18.671407",
        "description": "Перевод организации",
        "from": "Visa Platinum 1234567890123456",
        "to": "Счет 12345678901234567890",
        "operationAmount": {"amount": "100.500", "currency": {"name": "руб.", "code": "RUB"}},
    }
    print_operation(operation)
    captured = capsys.readouterr()
    assert "11.03.2024" in captured.out
    assert "Перевод организации" in captured.out
    assert "Сумма:" in captured.out
    assert "100.5" in captured.out
    assert "руб." in captured.out
    assert "->" in captured.out


def test_print_operation_without_from(capsys):
    operation = {
        "date": "2024-03-11T02:26:18.671407",
        "description": "Открытие вклада",
        "to": "Счет 12345678901234567890",
        "operationAmount": {"amount": "50000", "currency": {"name": "руб.", "code": "RUB"}},
    }
    print_operation(operation)
    captured = capsys.readouterr()
    assert "Счет **7890" in captured.out
    assert "->" not in captured.out


def test_print_operation_without_to(capsys):
    operation = {
        "date": "2024-03-11T02:26:18.671407",
        "description": "Пополнение",
        "from": "Visa Platinum 1234567890123456",
        "operationAmount": {"amount": "10000", "currency": {"name": "USD", "code": "USD"}},
    }
    print_operation(operation)
    captured = capsys.readouterr()
    assert "Visa Platinum" in captured.out
    assert "->" in captured.out


@patch("main.input_int")
@patch("main.print_message")
@patch("main.print_program_message")
def test_choose_source_json(mock_print_prog, mock_print, mock_input_int):
    mock_input_int.return_value = 1
    func, file_name = choose_source()
    assert func.__name__ == "read_json_file"
    assert file_name == "data/operations.json"


@patch("main.input_int")
@patch("main.print_message")
@patch("main.print_program_message")
def test_choose_source_csv(mock_print_prog, mock_print, mock_input_int):
    mock_input_int.return_value = 2
    func, file_name = choose_source()
    assert func.__name__ == "get_transactions_csv"
    assert file_name == "data/transactions.csv"


@patch("main.input_int")
@patch("main.print_message")
@patch("main.print_program_message")
def test_choose_source_excel(mock_print_prog, mock_print, mock_input_int):
    mock_input_int.return_value = 3
    func, file_name = choose_source()
    assert func.__name__ == "get_transactions_excel"
    assert file_name == "data/transactions_excel.xlsx"
