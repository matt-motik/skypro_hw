# SkyPro_HW
Учебный проект. Представляет собой частичную реализацию некоторых банковских сервисов.
Это консольное приложение для анализа и фильтрации банковских транзакций. Программа поддерживает загрузку данных из JSON, CSV и Excel файлов, предоставляя пользователю гибкие инструменты для работы с финансовыми операциями.
### 🚀 Возможности программы

- **Множественные источники данных** — загрузка транзакций из JSON, CSV и Excel файлов
- **Фильтрация по статусу** — отбор операций по статусу (EXECUTED, CANCELED, PENDING) с автоматическим приведением регистра
- **Сортировка по дате** — упорядочивание транзакций по возрастанию или убыванию даты
- **Фильтрация по валюте** — отображение только рублевых транзакций
- **Поиск по описанию** — фильтрация операций по ключевым словам с использованием регулярных выражений
- **Маскировка конфиденциальных данных** — скрытие номеров карт и счетов при выводе
- **Красивый вывод** — цветное форматирование таблиц и транзакций в консоли
- **Логирование** — автоматическое сохранение всех действий в log-файлы

## Содержание
- [Технологии](#технологии)
- [Установка](#установка)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [Deploy и CI/CD](#deploy-и-cicd)
- [Contributing](#contributing)
- [FAQ](#faq)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)


<div id="технологии"></div>

## Технологии
- [Python](https://www.python.org/)
- **pandas** - обработка Excel файлов
- **requests** - HTTP-запросы к API конвертации валют
- **pytest** - тестирование с покрытием
- **poetry** - управление зависимостями

<div id="установка"></div>

## Установка
Для управления зависимостями в проекте используется [Poetry](https://python-poetry.org).

1. Клонируйте репозиторий:
```
git clone https://github.com/matt-motik/skypro_hw.git
cd skypro_hw
poetry install
```

<div id="разработка"></div>

## Разработка
<!-- СЕКЦИЯ_AUTO_API: СТАРТ -->
### 📚 Документация API

*Этот раздел генерируется автоматически из docstring.*

| Модуль | Функция/Класс | Краткое описание |
|--------|---------------|------------------|
| [**`decorators.py`**](docs/api/decorators.md) | | |
| | [🔧 log](docs/api/decorators.md#log) | Декоратор для логирования вызовов функций. |
| | [🔧 decorator](docs/api/decorators.md#decorator) | Декоратор для обёртки функции. |
| | [🔧 wrapper](docs/api/decorators.md#wrapper) | Обёртка, выполняющая логирование. |
| [**`external_api.py`**](docs/api/external_api.md) | | |
| | [🔧 convert_currency](docs/api/external_api.md#convert_currency) | Функция конвертации валюты. |
| [**`generators.py`**](docs/api/generators.md) | | |
| | [🔧 filter_by_currency](docs/api/generators.md#filter_by_currency) | Фильтрует транзакции по значению ключа 'currency'. |
| | [🔧 transaction_descriptions](docs/api/generators.md#transaction_descriptions) | Возвращает описание каждой операции по очереди. |
| | [🔧 card_number_generator](docs/api/generators.md#card_number_generator) | Генератор выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где Х — цифра номера карты. |
| [**`main.py`**](docs/api/main.md) | | |
| | [🔧 print_message](docs/api/main.md#print_message) | Печать сообщения. (Жёлтым)text. |
| | [🔧 print_program_message](docs/api/main.md#print_program_message) | Печать сообщения. "Программа: text". |
| | [🔧 input_int](docs/api/main.md#input_int) | Защищённый ввод целого числа. |
| | [🔧 choose_source](docs/api/main.md#choose_source) | Выбор источника данных. |
| | [🔧 input_choice](docs/api/main.md#input_choice) | Защищённый ввод из списка. |
| | [🔧 choose_status](docs/api/main.md#choose_status) | Выбирает статус для фильтрации. |
| | [🔧 print_operation](docs/api/main.md#print_operation) | Красивая печать операций в требуемом виде. |
| [**`masks.py`**](docs/api/masks.md) | | |
| | [🔧 get_mask_card_number](docs/api/masks.md#get_mask_card_number) | Маскирует номер карты. |
| | [🔧 get_mask_account](docs/api/masks.md#get_mask_account) | Маскирует номер счета. |
| [**`processing.py`**](docs/api/processing.md) | | |
| | [🔧 filter_by_state](docs/api/processing.md#filter_by_state) | Фильтрует операции по значению ключа 'state'. |
| | [🔧 sort_by_date](docs/api/processing.md#sort_by_date) | Сортирует операции по дате. |
| | [🔧 process_bank_search](docs/api/processing.md#process_bank_search) | Функция поиска операций по описанию. |
| | [🔧 process_bank_operations](docs/api/processing.md#process_bank_operations) | Функция для подсчета количества банковских операций определенного типа. |
| [**`transactions_readers.py`**](docs/api/transactions_readers.md) | | |
| | [🔧 get_transactions_csv](docs/api/transactions_readers.md#get_transactions_csv) | Функция для считывания финансовых операций из CSV. |
| | [🔧 get_transactions_excel](docs/api/transactions_readers.md#get_transactions_excel) | Функция для считывания финансовых операций из Excel. |
| | [🔧 convert_to_operation](docs/api/transactions_readers.md#convert_to_operation) | Приводит транзакции к единому формату с операциями. |
| [**`utils.py`**](docs/api/utils.md) | | |
| | [🔧 linearize_operation](docs/api/utils.md#linearize_operation) | Приводит операции к единому формату с транзакциями. |
| | [🔧 read_json_file](docs/api/utils.md#read_json_file) | Функция чтения JSON-файла. |
| | [🔧 get_amount_in_rub](docs/api/utils.md#get_amount_in_rub) | Функция конвертации валюты из USD и EUR в рубли. |
| [**`widget.py`**](docs/api/widget.md) | | |
| | [🔧 mask_account_card](docs/api/widget.md#mask_account_card) | Маскирует номер карты или счета в строке. |
| | [🔧 get_date](docs/api/widget.md#get_date) | Преобразует дату из ISO формата в формат ДД.ММ.ГГГГ. |

> 📘 **Полная документация** с примерами и описанием параметров доступна в папке [`docs/api`](docs/api).

<!-- СЕКЦИЯ_AUTO_API: КОНЕЦ -->
### Требования
В разработке
### Установка зависимостей
```poetry install```
### Запуск программы
```poetry run python main.py```
### Создание билда
В разработке

<div id="тестирование"></div>

## 🧪 Тестирование
<!-- СЕКЦИЯ_AUTO_TEST: СТАРТ -->

*Этот раздел генерируется автоматически на основании данных `poetry run pytest`.*

### 📊 Результаты тестов SRC

```
📈 Покрытие кода:
tests/test_decorators.py ....                                            [  3%]
tests/test_external_api.py ..                                            [  4%]
tests/test_generators.py ...................                             [ 19%]
tests/test_main.py ...............                                       [ 31%]
tests/test_masks.py ..............                                       [ 42%]
tests/test_processing.py ...................                             [ 57%]
tests/test_transactions_readers.py ...............                       [ 69%]
tests/test_utils.py ............                                         [ 78%]
tests/test_widget.py ...........................                         [100%]
src/__init__.py                   0      0   100%
src/decorators.py                37      0   100%
src/external_api.py              34      0   100%
src/generators.py                35      0   100%
src/masks.py                     29      0   100%
src/processing.py                37      0   100%
src/transactions_readers.py      64      0   100%
src/utils.py                     68      0   100%
src/widget.py                    32      0   100%
TOTAL                           336      0   100%
Coverage HTML written to dir htmlcov/src

🎯 Результаты тестов src:
tests/test_decorators.py ....                                            [  3%]
tests/test_external_api.py ..                                            [  4%]
tests/test_generators.py ...................                             [ 19%]
tests/test_main.py ...............                                       [ 31%]
tests/test_masks.py ..............                                       [ 42%]
tests/test_processing.py ...................                             [ 57%]
tests/test_transactions_readers.py ...............                       [ 69%]
tests/test_utils.py ............                                         [ 78%]
tests/test_widget.py ...........................                         [100%]
================================ tests coverage ================================
-----------------------------------------------------------
-----------------------------------------------------------
============================= 127 passed in 0.50s ==============================
```

> 📊 **HTML отчёт покрытия**: [`htmlcov/index.html`](htmlcov/src/index.html)

### 📊 Результаты тестов maim.py

```
📈 Покрытие кода:
tests/test_main.py ...............                                       [100%]
main.py     100      0   100%
TOTAL       100      0   100%
Coverage HTML written to dir htmlcov/main

🎯 Результаты тестов main.py:
============================= test session starts ==============================
tests/test_main.py ...............                                       [100%]
================================ tests coverage ================================
---------------------------------------
---------------------------------------
============================== 15 passed in 0.28s ==============================
```

> 📊 **HTML отчёт покрытия**: [`htmlcov/index.html`](htmlcov/main/index.html)



<!-- СЕКЦИЯ_AUTO_TEST: КОНЕЦ -->
## Deploy и CI/CD
В разработке


## Contributing
В разработке — [Contributing.md](./CONTRIBUTING.md).

## FAQ
В разработке

## To do
- [x] Добавить крутое README
- [x] Сделать скрипт для генерации документации API на основе docstring
- [x] Написать тесты к модулям
- [x] Доработать скрипт генерации README для testcoverage 
- [x] Написать generators.py и test_generators.py
- [x] Написать utils.py и test_utils.py
- [x] Написать external_api.py и test_external_api.py
- [x] Добавить шаблон .env.example и работу с .env
- [x] Добавить логирование в модули masks и utils
- [x] Написать transactions_readers.py и test_transactions_readers.py
- [x] Написать process_bank_operations и и тесты
- [x] Написать process_bank_search и и тесты
- [x] Написать логику в main и и тесты
- [x] Доработать скрипт генерации README для main и src
- [x] Обновить документацию

## Команда проекта
- Matvey Bakirov — [mabakirov@gmail.com](mailto:mabakirov@gmail.com) — Back-End Engineer
 