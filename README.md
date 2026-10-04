# Qazaq Inflector

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![PyPI version](https://img.shields.io/pypi/v/qazaq_inflector.svg)](https://pypi.org/project/qazaq_inflector)
[![Tests](https://github.com/zhandos717/qazaq_inflector/actions/workflows/tests.yml/badge.svg)](https://github.com/zhandos717/qazaq_inflector/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A dependency-free Python library for declining Kazakh first names, full names and personal pronouns across all seven grammatical cases.

[Русская версия](README_RU.md) · [Қазақша нұсқасы](README_KZ.md)

## Features

- All seven Kazakh cases: `nominative`, `genitive`, `dative`, `accusative`, `locative`, `ablative`, `instrumental`
- Vowel harmony (back/front vowels) and suffix choice by the final sound: vowel, nasal (`м н ң`), sonorant (`л р й у и`), `ж з`, voiceless consonant
- Russian-style surnames (`-ов`, `-ев`, `-ова`, `-ева`) take harmony from the Kazakh stem: `Құнанбаев → Құнанбаевқа`
- Full names: every space-separated part is declined, patronymics ending in `ұлы` / `қызы` stay unchanged
- Hyphenated double names: only the last part takes the suffix
- Personal pronouns `мен`, `сен`, `сіз`, `біз`, `ол` with their irregular forms
- Plural forms: `-лар/-лер`, `-дар/-дер`, `-тар/-тер`
- Full declension table via `declension()`

## Installation

```bash
pip install qazaq-inflector
```

## Quick start

```python
from qazaq_inflector import QazaqNameInflector

inflector = QazaqNameInflector()

inflector.inflect("Нұрлан", "genitive")          # Нұрланның
inflector.inflect("Нұрлан", "locative")          # Нұрланда
inflector.inflect("Нұрлан", "ablative")          # Нұрланнан
inflector.inflect("Сәуле", "accusative")         # Сәулені

inflector.inflect("Абай Құнанбаев", "dative")    # Абайға Құнанбаевқа
inflector.inflect("Ахмет Байтұрсынұлы", "genitive")  # Ахметтің Байтұрсынұлы

inflector.inflect("Мен", "ablative")             # Менен
inflector.inflect("Сіз", "instrumental")         # Сізбен

inflector.pluralize("Арна")                      # Арналар
inflector.pluralize("Бақыт")                     # Бақыттар

for case, (singular, plural) in inflector.declension("Нұрлан").items():
    print(f"{case}: {singular} / {plural}")
```

## Suffix table

| Case | After vowel | After `м н ң` | After `л р й у и`, `ж з` | After voiceless |
|---|---|---|---|---|
| genitive | -ның/-нің | -ның/-нің | -дың/-дің | -тың/-тің |
| dative | -ға/-ге | -ға/-ге | -ға/-ге | -қа/-ке |
| accusative | -ны/-ні | -ды/-ді | -ды/-ді | -ты/-ті |
| locative | -да/-де | -да/-де | -да/-де | -та/-те |
| ablative | -дан/-ден | -нан/-нен | -дан/-ден | -тан/-тен |
| instrumental | -мен | -мен | -мен (`ж з`: -бен) | -пен |

## API

### `inflect(name: Optional[str], case: str) -> Optional[str]`
Declines `name` into `case`. Returns `None` for `None`, the input unchanged for an empty string or an unknown case.

### `pluralize(name: str) -> str`
Returns the plural form of `name`.

### `declension(name: str) -> Dict[str, Tuple[str, str]]`
Returns `{case: (singular, plural)}` for all seven cases.

### `QazaqNameInflector.CASES`
Tuple of supported case names in grammatical order.

## Development

```bash
git clone https://github.com/zhandos717/qazaq_inflector.git
cd qazaq_inflector
pip install -e ".[dev]"
pytest
```

## License

[MIT](LICENSE) © Zhandos Zhandarbekov
