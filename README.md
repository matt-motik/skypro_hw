# SkyPro_HW
Учебный проект. Представляет собой частичую реализациюю некоторых банковских сервисов. (в разработке)

## Содержание
- [Технологии](#технологии)
- [Установка](#установка)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [Deploy и CI/CD](#deploy-и-cicd)
- [Contributing](#contributing)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Технологии
- [Python](https://www.python.org/)


## Установка
Для управления зависимостями в проекте используется [Poetry](https://python-poetry.org).

1. Клонируйте репозиторий:
```
git clone https://github.com/matt-motik/skypro_hw.git
cd skypro_hw
poetry install
```

## Разработка
<!-- СЕКЦИЯ_AUTO_API: СТАРТ -->
### 📚 Документация API

*Этот раздел генерируется автоматически из docstring.*

| Модуль | Функция/Класс | Краткое описание |
|--------|---------------|------------------|
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
## Тестирование
В разработке
## Deploy и CI/CD
В разработке

## Contributing
В разработке — [Contributing.md](./CONTRIBUTING.md).

## FAQ 
В разработке

## To do
- [x] Добавить крутое README
- [x] Сделать скрипт для генерации документации API на основе docstring
- [ ] Дооформить и сдать домашку

## Команда проекта
- [Matvey Bakirov](mailto:mabakirov@gmail.com) — Back-End Engineer
 