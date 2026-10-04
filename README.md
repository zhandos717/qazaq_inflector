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
- Possessive forms for all persons with case endings: `Арнама`, `Нұрланының`, `Арналарыңыз`
- Several possessed items: `Арналарым`, `Нұрландары`
- Possessive phrases: `Нұрланның әкесі`, `менің кітабым`
- Final `п/к/қ` voicing before vowels: `кітабы`, `Сұлтанбегі`
- Optional strict mode that raises `ValueError` on typos in case or person names
- Ships type hints (`py.typed`)
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

inflector.possessive("Арна", "1sg")              # Арнам
inflector.possessive("Арна", "1sg", "dative")    # Арнама
inflector.possessive("Нұрлан", "3", "genitive")  # Нұрланының
inflector.possessive("Арна", "1sg", plural=True)  # Арналарым

inflector.genitive_phrase("Нұрлан", "әке")              # Нұрланның әкесі
inflector.genitive_phrase("Нұрлан", "әке", "dative")    # Нұрланның әкесіне
inflector.genitive_phrase("мен", "кітап")               # менің кітабым

QazaqNameInflector(strict=True).inflect("Нұрлан", "dativ")  # ValueError: Unknown case 'dativ'

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

### `possessive(name: str, person: str = "3", case: str = "nominative", plural: bool = False) -> str`
Returns the possessive form of `name` in the given case. `plural=True` marks several possessed items. `person` is one of:

| person | owner | after vowel | after consonant |
|---|---|---|---|
| `1sg` | менің | -м | -ым/-ім |
| `2sg` | сенің | -ң | -ың/-ің |
| `2sg_formal` | сіздің | -ңыз/-ңіз | -ыңыз/-іңіз |
| `1pl` | біздің | -мыз/-міз | -ымыз/-іміз |
| `2pl` | сендердің | -ларың/-лерің (plural + 2sg) | |
| `2pl_formal` | сіздердің | -ларыңыз/-леріңіз (plural + 2sg_formal) | |
| `3` | оның / олардың | -сы/-сі | -ы/-і |

After the 3rd-person suffix cases take the pronominal `-н-` (`Нұрланына`, `Нұрланын`); after `-м`/`-ң` the dative is `-а/-е` (`Арнама`, `Арнаңа`). In a full name only the last part changes.

### `genitive_phrase(owner: str, thing: str, case: str = "nominative", plural: bool = False) -> str`
Builds the "owner's thing" phrase: owner in genitive, thing with the matching possessive suffix and `case`. A pronoun owner sets the person: `мен → менің кітабым`.

### `QazaqNameInflector(strict: bool = False)`
With `strict=True`, an unknown case or person raises `ValueError` instead of returning the input unchanged.

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

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE) © Zhandos Zhandarbekov
