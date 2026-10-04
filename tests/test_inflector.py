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
