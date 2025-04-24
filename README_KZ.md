# Qazaq inflector

**Qazaq Inflector** — қазақ есімдерін, толық ФИО-ны және жекеше есімдіктерді септеу үшін Python кітапханасы.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![PyPI version](https://img.shields.io/pypi/v/qazaq_inflector.svg)](https://pypi.org/project/qazaq_inflector)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Мүмкіндіктер

- Қазақ есімдерін барлық жеті септік бойынша септейді:
  - **атау (nominative)**, **ілік (genitive)**, **барыс (dative)**, **табыс (accusative)**, **жатыс (locative)**, **шығыс (ablative)**, **құрал (instrumental)**
- Толық ФИО (атасы/анасы суффикстері) тұрғызады:
  - `ұлы`, `қызы` деген жақтауықтары бар бөліктер өзгеріссіз қалады
  - ФИО әр сөзін пробел мен дефис арқылы сұрыптап, бөлек өңдейді
- Жекеше есімдіктерді (мен, біз, сен, сіз, ол) арнайы түрде септейді
- Көбейткіш сан (көпше түр) — `-дар`/`-дер`
- Барлық септіктерді кесте түрінде алуға мүмкіндік береді (`declension()` әдісі)

## Орнату

```bash
pip install qazaq-inflector
```

## Қолдану үлгісі

```python
from qazaq_inflector import QazaqNameInflector

inflector = QazaqNameInflector()

# Жалғыз есімді септеу
print(inflector.inflect("Нұрлан", "genitive"))      # Нұрланның
print(inflector.inflect("Нұрлан", "locative"))      # Нұрланнда

# Толық ФИО-ны септеу
print(inflector.inflect("Абай Құнанбаев", "dative"))  # Абайға Құнанбаевге

# Жекеше есімдіктерді септеу
print(inflector.inflect("Мен", "ablative"))          # Меннен
print(inflector.inflect("Сіз", "instrumental"))     # Сізбен

# Көпше түрді алу
print(inflector.pluralize("Нұрлан"))                  # Нұрландар

# Толық кестені алу
table = inflector.declension("Нұрлан")
for case, (sing, plur) in table.items():
    print(f"{case}: {sing} / {plur}")
```

## API

### `inflect(name: Optional[str], case: str) -> Optional[str]`
Берілген `name` жолын `case` септігіне сәйкес өңдейді. Егер `name` бос немесе `None` болса, бастапқы жол қайтарылады.

### `pluralize(name: str) -> str`
`name`-ге сәйкес көпше түрді (дар/дер) қайтарады.

### `declension(name: str) -> Dict[str, tuple]`
Есімнің барлық септік түрлерін сөздік ретінде қайтарады: `{ case: (жал.single, көпше) }`.

## Тестілеу

```bash
git clone https://github.com/zhandos717/qazaq_inflector.git
cd qazaq_inflector
pip install -e .[dev]
pytest
```

## Лицензия

Бұл жоба MIT лицензиясы бойынша таратылады — [LICENSE](LICENSE).

---

Автор: Zhandos Zhandarbekov  
Email: zhandos.zhandarbekov@gmail.com

