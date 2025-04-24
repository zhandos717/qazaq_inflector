# Qazaq Inflector

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![PyPI version](https://img.shields.io/pypi/v/qazaq_inflector.svg)](https://pypi.org/project/qazaq_inflector)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[//]: # ([![Build Status]&#40;https://github.com/zhandos717/qazaq_inflector/actions/workflows/python-package.yml/badge.svg&#41;]&#40;https://github.com/zhandos717/qazaq_inflector/actions&#41;)


Библиотека для склонения казахских имен и фамилий по падежам. Поддерживает 6 основных падежей казахского языка.

## Установка

Установите пакет через pip:

```bash
pip install qazaq_inflector
```

**Qazaq Inflector** — библиотека на Python для склонения казахских имён, ФИО и личных местоимений по падежам.

## Возможности

- Склоняет одиночные имена по всем семи казахским падежам:
  - `nominative`, `genitive`, `dative`, `accusative`, `locative`, `ablative`, `instrumental`
- Поддерживает фамилию, имя, отчество (ФИО):
  - части, оканчивающиеся на `ұлы` или `қызы` (патронимика) не склоняются
  - разбивает ФИО по пробелам и дефисам
- Склоняет личные местоимения: `мен`, `біз`, `сен`, `сіз`, `ол`
- Генерирует множественное число: `-дар`/`-дер`
- Формирует полную таблицу склонений через метод `declension()`

## Установка

```bash
pip install qazaq-inflector
```

## Быстрый старт

```python
from qazaq_inflector import QazaqNameInflector

inflector = QazaqNameInflector()

# Склонение одиночного имени
print(inflector.inflect("Нұрлан", "genitive"))       # Нұрланның
print(inflector.inflect("Нұрлан", "locative"))       # Нұрланнда

# Склонение ФИО
print(inflector.inflect("Абай Құнанбаев", "dative"))   # Абайға Құнанбаевге

# Склонение местоимений
print(inflector.inflect("Мен", "ablative"))           # Меннен
print(inflector.inflect("Сіз", "instrumental"))      # Сізбен

# Множественное число
print(inflector.pluralize("Нұрлан"))                   # Нұрландар

# Полная таблица
table = inflector.declension("Нұрлан")
for case, (sing, plur) in table.items():
    print(f"{case}: {sing} / {plur}")
```

## API

### `inflect(name: Optional[str], case: str) -> Optional[str]`
Склоняет `name` по падежу `case`. Если `name` равен `None` или пустая строка, возвращает оригинал.

### `pluralize(name: str) -> str`
Возвращает множественную форму `name` с учётом гармонии: `дар` или `дер`.

### `declension(name: str) -> Dict[str, tuple]`
Возвращает словарь всех падежей `{ case: (singular, plural) }`.

## Тесты

```bash
git clone https://github.com/zhandos717/qazaq_inflector.git
cd qazaq_inflector
pip install -e .[dev]
pytest
```

## Лицензия

Проект распространяется под лицензией [MIT](LICENSE).

---

Автор: Zhandos Zhandarbekov  
Email: zhandos.zhandarbekov@gmail.com




