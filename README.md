# SkyPro_HW
Учебный проект. Представляет собой частичную реализацию некоторых банковских сервисов. (в разработке)

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
| [**`generators.py`**](docs/api/generators.md) | | |
| | [🔧 filter_by_currency](docs/api/generators.md#filter_by_currency) | Фильтрует транзакции по значению ключа 'currency'. |
| | [🔧 transaction_descriptions](docs/api/generators.md#transaction_descriptions) | Возвращает описание каждой операции по очереди. |
| | [🔧 card_number_generator](docs/api/generators.md#card_number_generator) | Генератор выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где Х — цифра номера карты. |
| [**`masks.py`**](docs/api/masks.md) | | |
| | [🔧 get_mask_card_number](docs/api/masks.md#get_mask_card_number) | Маскирует номер карты. |
| | [🔧 get_mask_account](docs/api/masks.md#get_mask_account) | Маскирует номер счета. |
| [**`processing.py`**](docs/api/processing.md) | | |
| | [🔧 filter_by_state](docs/api/processing.md#filter_by_state) | Фильтрует операции по значению ключа 'state'. |
| | [🔧 sort_by_date](docs/api/processing.md#sort_by_date) | Сортирует операции по дате. |
| [**`widget.py`**](docs/api/widget.md) | | |
| | [🔧 mask_account_card](docs/api/widget.md#mask_account_card) | Маскирует номер карты или счета в строке. |
| | [🔧 get_date](docs/api/widget.md#get_date) | Преобразует дату из ISO формата в формат ДД.ММ.ГГГГ. |

> 📘 **Полная документация** с примерами и описанием параметров доступна в папке [`docs/api`](docs/api).

<!-- СЕКЦИЯ_AUTO_API: КОНЕЦ -->
### Требования
В разработке
### Установка зависимостей
В разработке
### Запуск Development сервера
В разработке
### Создание билда
В разработке

<div id="тестирование"></div>

## 🧪 Тестирование
<!-- СЕКЦИЯ_AUTO_TEST: СТАРТ -->

*Этот раздел генерируется автоматически на основании данных `poetry run pytest`.*

### 📊 Результаты тестов

```
📈 Покрытие кода:
tests/test_decorators.py ....                                            [  5%]
tests/test_generators.py ...................                             [ 29%]
tests/test_masks.py ..............                                       [ 46%]
tests/test_processing.py ...............                                 [ 65%]
tests/test_widget.py ...........................                         [100%]
src/__init__.py         0      0   100%
src/decorators.py      37      0   100%
src/generators.py      35      0   100%
src/masks.py           14      0   100%
src/processing.py       9      0   100%
src/widget.py          32      0   100%
TOTAL                 127      0   100%
Coverage HTML written to dir htmlcov

🎯 Результаты тестов:
============================= test session starts ==============================
tests/test_decorators.py ....                                            [  5%]
tests/test_generators.py ...................                             [ 29%]
tests/test_masks.py ..............                                       [ 46%]
tests/test_processing.py ...............                                 [ 65%]
tests/test_widget.py ...........................                         [100%]
================================ tests coverage ================================
-------------------------------------------------
-------------------------------------------------
============================== 79 passed in 0.10s ==============================
```

> 📊 **HTML отчёт покрытия**: [`htmlcov/index.html`](htmlcov/index.html)



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
- [x] Написать decorators.py и test_decorators.py
- [x] Обновить документацию

## Команда проекта
- Matvey Bakirov — [mabakirov@gmail.com](mailto:mabakirov@gmail.com) — Back-End Engineer
 