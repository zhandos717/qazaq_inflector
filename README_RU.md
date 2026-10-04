# Qazaq Inflector

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![PyPI version](https://img.shields.io/pypi/v/qazaq_inflector.svg)](https://pypi.org/project/qazaq_inflector)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Qazaq Inflector** — библиотека на Python для склонения казахских имён, ФИО и личных местоимений по падежам.

[English](README.md) · [Қазақша](README_KZ.md)

## Возможности

- Склоняет одиночные имена по всем семи казахским падежам:
  - `nominative`, `genitive`, `dative`, `accusative`, `locative`, `ablative`, `instrumental`
- Поддерживает фамилию, имя, отчество (ФИО):
  - части, оканчивающиеся на `ұлы` или `қызы` (патронимика) не склоняются
  - в ФИО через пробел склоняется каждая часть, в двойном имени через дефис — только последняя
- Склоняет личные местоимения: `мен`, `біз`, `сен`, `сіз`, `ол`
- Генерирует множественное число: `-лар/-лер`, `-дар/-дер`, `-тар/-тер`
- Притяжательные формы всех лиц с падежами: `Арнама`, `Нұрланының`, `Сәулесіне`
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
print(inflector.inflect("Нұрлан", "locative"))       # Нұрланда

# Склонение ФИО
print(inflector.inflect("Абай Құнанбаев", "dative"))   # Абайға Құнанбаевқа

# Склонение местоимений
print(inflector.inflect("Мен", "ablative"))           # Менен
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
Склоняет `name` по падежу `case`. Для `None` возвращает `None`, для пустой строки или неизвестного падежа — исходное значение.

### `pluralize(name: str) -> str`
Возвращает множественную форму `name` с учётом гармонии и последнего звука: `-лар`, `-дар` или `-тар`.

### `possessive(name: str, person: str = "3", case: str = "nominative", plural: bool = False) -> str`
Притяжательная форма в нужном падеже. `person`: `1sg` (менің), `2sg` (сенің), `2sg_formal` (сіздің), `1pl` (біздің), `2pl` (сендердің), `2pl_formal` (сіздердің), `3` (оның). `plural=True`: `Арналарым`. Пример: `possessive("Арна", "1sg", "dative")` → `Арнама`.

### `genitive_phrase(owner, thing, case="nominative", plural=False) -> str`
Изафет «чьё-то что-то»: `genitive_phrase("Нұрлан", "әке")` → `Нұрланның әкесі`, `genitive_phrase("мен", "кітап")` → `менің кітабым`.

### `QazaqNameInflector(strict=False)`
При `strict=True` неизвестный падеж или лицо вызывает `ValueError`.

### `declension(name: str) -> Dict[str, tuple]`
Возвращает словарь всех падежей `{ case: (singular, plural) }`.

## Тесты

```bash
git clone https://github.com/zhandos717/qazaq_inflector.git
cd qazaq_inflector
pip install -e ".[dev]"
pytest
```

## Лицензия

Проект распространяется под лицензией [MIT](LICENSE).

---

Автор: Zhandos Zhandarbekov  
Email: zhandos.zhandarbekov@gmail.com
