import pytest

from qazaq_inflector import QazaqNameInflector


@pytest.fixture
def inflector():
    return QazaqNameInflector()


@pytest.mark.parametrize('case, expected', [
    ('nominative', 'Нұрлан'),
    ('genitive', 'Нұрланның'),
    ('dative', 'Нұрланға'),
    ('accusative', 'Нұрланды'),
    ('locative', 'Нұрланда'),
    ('ablative', 'Нұрланнан'),
    ('instrumental', 'Нұрланмен'),
])
def test_all_cases_for_nasal_ending(inflector, case, expected):
    assert inflector.inflect('Нұрлан', case) == expected


@pytest.mark.parametrize('name, case, expected', [
    ('Арна', 'genitive', 'Арнаның'),
    ('Арна', 'accusative', 'Арнаны'),
    ('Сәуле', 'genitive', 'Сәуленің'),
    ('Сәуле', 'accusative', 'Сәулені'),
    ('Сәуле', 'ablative', 'Сәуледен'),
    ('Айгүл', 'genitive', 'Айгүлдің'),
    ('Абай', 'accusative', 'Абайды'),
    ('Әли', 'genitive', 'Әлидің'),
    ('Әли', 'accusative', 'Әлиді'),
    ('Аян', 'accusative', 'Аянды'),
    ('Ерлан', 'ablative', 'Ерланнан'),
    ('Ержан', 'genitive', 'Ержанның'),
    ('Мейрам', 'ablative', 'Мейрамнан'),
    ('Мәдина', 'ablative', 'Мәдинадан'),
    ('Айбаз', 'instrumental', 'Айбазбен'),
    ('Сұлтанбек', 'instrumental', 'Сұлтанбекпен'),
    ('Бақыт', 'dative', 'Бақытқа'),
    ('Ләззат', 'dative', 'Ләззатқа'),
    ('Дәулет', 'locative', 'Дәулетте'),
    ('Дәулет', 'genitive', 'Дәулеттің'),
    ('Асқар', 'locative', 'Асқарда'),
])
def test_ending_classes_and_harmony(inflector, name, case, expected):
    assert inflector.inflect(name, case) == expected


@pytest.mark.parametrize('surname, case, expected', [
    ('Құнанбаев', 'dative', 'Құнанбаевқа'),
    ('Құнанбаев', 'genitive', 'Құнанбаевтың'),
    ('Назарбаева', 'genitive', 'Назарбаеваның'),
    ('Әлиев', 'dative', 'Әлиевке'),
])
def test_russian_style_surnames(inflector, surname, case, expected):
    assert inflector.inflect(surname, case) == expected


def test_full_name_with_space(inflector):
    assert inflector.inflect('Абай Құнанбаев', 'dative') == 'Абайға Құнанбаевқа'


def test_patronymic_is_not_inflected(inflector):
    assert inflector.inflect('Ахмет Байтұрсынұлы', 'genitive') == 'Ахметтің Байтұрсынұлы'


def test_hyphenated_name_inflects_last_part(inflector):
    assert inflector.inflect('Гүлнар-Баян', 'locative') == 'Гүлнар-Баянда'


@pytest.mark.parametrize('word, case, expected', [
    ('Мен', 'ablative', 'Менен'),
    ('Сіз', 'instrumental', 'Сізбен'),
    ('ол', 'genitive', 'оның'),
    ('сен', 'dative', 'саған'),
])
def test_pronouns(inflector, word, case, expected):
    assert inflector.inflect(word, case) == expected


@pytest.mark.parametrize('name, expected', [
    ('Арна', 'Арналар'),
    ('Сәуле', 'Сәулелер'),
    ('Асқар', 'Асқарлар'),
    ('Айгүл', 'Айгүлдер'),
    ('Нұрлан', 'Нұрландар'),
    ('Айбаз', 'Айбаздар'),
    ('Бақыт', 'Бақыттар'),
    ('Дәулет', 'Дәулеттер'),
])
def test_pluralize(inflector, name, expected):
    assert inflector.pluralize(name) == expected


def test_declension_table(inflector):
    table = inflector.declension('Нұрлан')
    assert list(table) == list(QazaqNameInflector.CASES)
    assert table['genitive'] == ('Нұрланның', 'Нұрландардың')
    assert table['ablative'] == ('Нұрланнан', 'Нұрландардан')


def test_uppercase_word_gets_uppercase_suffix(inflector):
    assert inflector.inflect('НҰРЛАН', 'genitive') == 'НҰРЛАННЫҢ'


def test_empty_and_none(inflector):
    assert inflector.inflect('', 'genitive') == ''
    assert inflector.inflect(None, 'dative') is None


def test_invalid_case_returns_word(inflector):
    assert inflector.inflect('Нұрлан', 'unknown') == 'Нұрлан'


@pytest.mark.parametrize('name, person, expected', [
    ('Арна', '1sg', 'Арнам'),
    ('Арна', '2sg', 'Арнаң'),
    ('Арна', '2sg_formal', 'Арнаңыз'),
    ('Арна', '1pl', 'Арнамыз'),
    ('Арна', '3', 'Арнасы'),
    ('Нұрлан', '1sg', 'Нұрланым'),
    ('Нұрлан', '2sg_formal', 'Нұрланыңыз'),
    ('Нұрлан', '1pl', 'Нұрланымыз'),
    ('Нұрлан', '3', 'Нұрланы'),
    ('Сәуле', '3', 'Сәулесі'),
    ('Дәулет', '1sg', 'Дәулетім'),
    ('Дәулет', '3', 'Дәулеті'),
])
def test_possessive_nominative(inflector, name, person, expected):
    assert inflector.possessive(name, person) == expected


@pytest.mark.parametrize('name, person, case, expected', [
    ('Арна', '1sg', 'dative', 'Арнама'),
    ('Сәуле', '2sg', 'dative', 'Сәулеңе'),
    ('Арна', '1sg', 'genitive', 'Арнамның'),
    ('Арна', '1sg', 'accusative', 'Арнамды'),
    ('Арна', '1sg', 'ablative', 'Арнамнан'),
    ('Арна', '1pl', 'dative', 'Арнамызға'),
    ('Арна', '2sg_formal', 'instrumental', 'Арнаңызбен'),
    ('Нұрлан', '3', 'genitive', 'Нұрланының'),
    ('Нұрлан', '3', 'dative', 'Нұрланына'),
    ('Нұрлан', '3', 'accusative', 'Нұрланын'),
    ('Нұрлан', '3', 'locative', 'Нұрланында'),
    ('Нұрлан', '3', 'ablative', 'Нұрланынан'),
    ('Нұрлан', '3', 'instrumental', 'Нұрланымен'),
    ('Сәуле', '3', 'dative', 'Сәулесіне'),
])
def test_possessive_with_case(inflector, name, person, case, expected):
    assert inflector.possessive(name, person, case) == expected


def test_possessive_full_name_changes_last_part(inflector):
    assert inflector.possessive('Абай Құнанбаев', '1sg', 'dative') == 'Абай Құнанбаевыма'


def test_possessive_unknown_person_returns_word(inflector):
    assert inflector.possessive('Арна', '5') == 'Арна'
