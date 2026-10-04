# Qazaq inflector

**Qazaq Inflector** — қазақ есімдерін, толық ФИО-ны және жекеше есімдіктерді септеу үшін Python кітапханасы.

[English](README.md) · [Русский](README_RU.md)

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![PyPI version](https://img.shields.io/pypi/v/qazaq_inflector.svg)](https://pypi.org/project/qazaq_inflector)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Мүмкіндіктер

- Қазақ есімдерін барлық жеті септік бойынша септейді:
  - **атау (nominative)**, **ілік (genitive)**, **барыс (dative)**, **табыс (accusative)**, **жатыс (locative)**, **шығыс (ablative)**, **құрал (instrumental)**
- Толық ФИО (атасы/анасы суффикстері) тұрғызады:
  - `ұлы`, `қызы` деген жақтауықтары бар бөліктер өзгеріссіз қалады
  - ФИО әр сөзін пробел мен дефис арқылы сұрыптап, бөлек өңдейді
- Жекеше есімдіктерді (мен, біз, сен, сіз, ол) арнайы түрде септейді
- Көбейткіш сан (көпше түр) — `-лар/-лер`, `-дар/-дер`, `-тар/-тер`
- Тәуелдік жалғаулары барлық жақта, септікпен бірге: `Арнама`, `Нұрланының`, `Сәулесіне`
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
print(inflector.inflect("Нұрлан", "locative"))      # Нұрланда

# Толық ФИО-ны септеу
print(inflector.inflect("Абай Құнанбаев", "dative"))  # Абайға Құнанбаевқа

# Жекеше есімдіктерді септеу
print(inflector.inflect("Мен", "ablative"))          # Менен
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
`name`-ге сәйкес көпше түрді (-лар/-дар/-тар) қайтарады.

### `possessive(name: str, person: str = "3", case: str = "nominative", plural: bool = False) -> str`
Тәуелдік түрін септікпен қайтарады. `person`: `1sg` (менің), `2sg` (сенің), `2sg_formal` (сіздің), `1pl` (біздің), `2pl` (сендердің), `2pl_formal` (сіздердің), `3` (оның). `plural=True`: `Арналарым`. Мысалы: `possessive("Арна", "1sg", "dative")` → `Арнама`.

### `genitive_phrase(owner, thing, case="nominative", plural=False) -> str`
Ілік септікті тіркес: `genitive_phrase("Нұрлан", "әке")` → `Нұрланның әкесі`, `genitive_phrase("мен", "кітап")` → `менің кітабым`.

### `QazaqNameInflector(strict=False)`
`strict=True` болса, белгісіз септік не жақ үшін `ValueError` шығады.

### `declension(name: str) -> Dict[str, tuple]`
Есімнің барлық септік түрлерін сөздік ретінде қайтарады: `{ case: (жал.single, көпше) }`.

## Тестілеу

```bash
git clone https://github.com/zhandos717/qazaq_inflector.git
cd qazaq_inflector
pip install -e ".[dev]"
pytest
```

## Лицензия

Бұл жоба MIT лицензиясы бойынша таратылады — [LICENSE](LICENSE).

---

Автор: Zhandos Zhandarbekov  
Email: zhandos.zhandarbekov@gmail.com
