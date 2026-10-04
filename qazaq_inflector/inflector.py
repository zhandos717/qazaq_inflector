from typing import Dict, Optional, Tuple


class QazaqNameInflector:
    """
    Инфлектор казахских имён, ФИО и местоимений: добавляет суффиксы падежей согласно гармонии гласных
    и классу последнего звука основы.

    Поддерживаемые падежи:
      - nominative   — атау
      - genitive     — ілік
      - dative       — барыс
      - accusative   — табыс
      - locative     — жатыс
      - ablative     — шығыс
      - instrumental — көмектес

    Особенности:
      - ФИО: части, оканчивающиеся на 'ұлы' или 'қызы', не склоняются.
      - В ФИО через пробел склоняется каждая часть, в двойном имени через дефис — только последняя.
      - Местоимения (мен, сен, сіз, ол, біз, сендер, сіздер, олар) имеют специальные формы.
    """

    CASES: Tuple[str, ...] = (
        'nominative', 'genitive', 'dative', 'accusative', 'locative', 'ablative', 'instrumental',
    )

    # и/у не задают твёрдость: они встречаются в словах обоих рядов
    _HARD_VOWELS = frozenset('аұыояюё')
    _SOFT_VOWELS = frozenset('әүіөеэ')
    # и/у на конце звучат как [ій]/[ұу] и присоединяют суффиксы как сонорные согласные
    _VOWELS = frozenset('аәеэоөұүыіяюё')
    _NASALS = frozenset('мнң')
    _SONORANTS = frozenset('лрйуи')
    _VOICED_SIBILANTS = frozenset('жз')
    # б, в, г, д на конце заимствований оглушаются: Құнанбаевқа, Ахмедке
    _VOICELESS = frozenset('кқпстфхцчшщбвгд')

    # Перед гласной глухие п, к, қ озвончаются: кітап → кітабы, Сұлтанбек → Сұлтанбегі
    _VOICING = {'п': 'б', 'к': 'г', 'қ': 'ғ', 'П': 'Б', 'К': 'Г', 'Қ': 'Ғ'}

    _PATRONYMIC_SUFFIXES = ('ұлы', 'қызы')
    # Гармонию мужских фамилий определяет основа: Құнанбаев → Құнанба-, Ахметов → Ахмет-.
    # В женских -ова/-ева гармонию задаёт конечная -а: Ахметоваға
    _SURNAME_SUFFIXES = ('ов', 'ев')

    _PRONOUNS: Dict[str, Dict[str, str]] = {
        'мен': {
            'nominative': 'мен', 'genitive': 'менің', 'dative': 'маған', 'accusative': 'мені',
            'locative': 'менде', 'ablative': 'менен', 'instrumental': 'менімен',
        },
        'біз': {
            'nominative': 'біз', 'genitive': 'біздің', 'dative': 'бізге', 'accusative': 'бізді',
            'locative': 'бізде', 'ablative': 'бізден', 'instrumental': 'бізбен',
        },
        'сен': {
            'nominative': 'сен', 'genitive': 'сенің', 'dative': 'саған', 'accusative': 'сені',
            'locative': 'сенде', 'ablative': 'сенен', 'instrumental': 'сенімен',
        },
        'сіз': {
            'nominative': 'сіз', 'genitive': 'сіздің', 'dative': 'сізге', 'accusative': 'сізді',
            'locative': 'сізде', 'ablative': 'сізден', 'instrumental': 'сізбен',
        },
        'ол': {
            'nominative': 'ол', 'genitive': 'оның', 'dative': 'оған', 'accusative': 'оны',
            'locative': 'онда', 'ablative': 'одан', 'instrumental': 'онымен',
        },
        'сендер': {
            'nominative': 'сендер', 'genitive': 'сендердің', 'dative': 'сендерге', 'accusative': 'сендерді',
            'locative': 'сендерде', 'ablative': 'сендерден', 'instrumental': 'сендермен',
        },
        'сіздер': {
            'nominative': 'сіздер', 'genitive': 'сіздердің', 'dative': 'сіздерге', 'accusative': 'сіздерді',
            'locative': 'сіздерде', 'ablative': 'сіздерден', 'instrumental': 'сіздермен',
        },
        'олар': {
            'nominative': 'олар', 'genitive': 'олардың', 'dative': 'оларға', 'accusative': 'оларды',
            'locative': 'оларда', 'ablative': 'олардан', 'instrumental': 'олармен',
        },
    }

    # Классы окончаний: vowel, nasal (м н ң), sonorant (л р й у и), voiced (ж з), voiceless
    _CASE_SUFFIXES: Dict[str, Dict[str, Tuple[str, str]]] = {
        'genitive': {
            'vowel': ('ның', 'нің'), 'nasal': ('ның', 'нің'), 'sonorant': ('дың', 'дің'),
            'voiced': ('дың', 'дің'), 'voiceless': ('тың', 'тің'),
        },
        'dative': {
            'vowel': ('ға', 'ге'), 'nasal': ('ға', 'ге'), 'sonorant': ('ға', 'ге'),
            'voiced': ('ға', 'ге'), 'voiceless': ('қа', 'ке'),
        },
        'accusative': {
            'vowel': ('ны', 'ні'), 'nasal': ('ды', 'ді'), 'sonorant': ('ды', 'ді'),
            'voiced': ('ды', 'ді'), 'voiceless': ('ты', 'ті'),
        },
        'locative': {
            'vowel': ('да', 'де'), 'nasal': ('да', 'де'), 'sonorant': ('да', 'де'),
            'voiced': ('да', 'де'), 'voiceless': ('та', 'те'),
        },
        'ablative': {
            'vowel': ('дан', 'ден'), 'nasal': ('нан', 'нен'), 'sonorant': ('дан', 'ден'),
            'voiced': ('дан', 'ден'), 'voiceless': ('тан', 'тен'),
        },
        'instrumental': {
            'vowel': ('мен', 'мен'), 'nasal': ('мен', 'мен'), 'sonorant': ('мен', 'мен'),
            'voiced': ('бен', 'бен'), 'voiceless': ('пен', 'пен'),
        },
    }

    # (после гласной, после согласной), каждый вариант — (твёрдый, мягкий)
    _POSSESSIVE_SUFFIXES: Dict[str, Tuple[Tuple[str, str], Tuple[str, str]]] = {
        '1sg': (('м', 'м'), ('ым', 'ім')),
        '2sg': (('ң', 'ң'), ('ың', 'ің')),
        '2sg_formal': (('ңыз', 'ңіз'), ('ыңыз', 'іңіз')),
        '1pl': (('мыз', 'міз'), ('ымыз', 'іміз')),
        '3': (('сы', 'сі'), ('ы', 'і')),
    }
    _PRONOUN_PERSONS = {
        'мен': '1sg', 'сен': '2sg', 'сіз': '2sg_formal', 'біз': '1pl',
        'сендер': '2pl', 'сіздер': '2pl_formal', 'ол': '3', 'олар': '3',
    }

    # Жіктік жалғау: (после гласной/сонорной, после ж/з, после глухой), каждый — (твёрдый, мягкий)
    _PREDICATE_SUFFIXES: Dict[str, Tuple[Tuple[str, str], ...]] = {
        '1sg': (('мын', 'мін'), ('бын', 'бін'), ('пын', 'пін')),
        '1pl': (('мыз', 'міз'), ('быз', 'біз'), ('пыз', 'піз')),
        '2sg': (('сың', 'сің'),) * 3,
        '2sg_formal': (('сыз', 'сіз'),) * 3,
        '2pl': (('сыңдар', 'сіңдер'),) * 3,
        '2pl_formal': (('сыздар', 'сіздер'),) * 3,
        '3': (('', ''),) * 3,
    }

    # Падежи после притяжательного суффикса 3-го лица идут через вставное -н-: Арнасына, Нұрланын
    _PRONOMINAL_CASE_SUFFIXES: Dict[str, Tuple[str, str]] = {
        'genitive': ('ның', 'нің'), 'dative': ('на', 'не'), 'accusative': ('н', 'н'),
        'locative': ('нда', 'нде'), 'ablative': ('нан', 'нен'), 'instrumental': ('мен', 'мен'),
    }

    _PLURAL_SUFFIXES: Dict[str, Tuple[str, str]] = {
        'vowel': ('лар', 'лер'), 'sonorant': ('лар', 'лер'), 'nasal': ('дар', 'дер'),
        'voiced': ('дар', 'дер'), 'voiceless': ('тар', 'тер'),
    }

    def __init__(self, strict: bool = False):
        """strict=True — ValueError на неизвестный падеж или лицо вместо возврата слова без изменений."""
        self.strict = strict

    def _is_hard(self, word: str) -> bool:
        lower = word.lower()
        for suffix in self._SURNAME_SUFFIXES:
            stem = lower[:-len(suffix)]
            if lower.endswith(suffix) and any(ch in self._HARD_VOWELS or ch in self._SOFT_VOWELS for ch in stem):
                lower = stem
                break
        for ch in reversed(lower):
            if ch in self._HARD_VOWELS:
                return True
            if ch in self._SOFT_VOWELS:
                return False
        return True

    def _ending_class(self, word: str) -> str:
        last = word[-1].lower()
        if last in self._VOWELS:
            return 'vowel'
        if last in self._NASALS:
            return 'nasal'
        if last in self._VOICED_SIBILANTS:
            return 'voiced'
        if last in self._VOICELESS:
            return 'voiceless'
        return 'sonorant'

    def _add_suffix(self, word: str, variants: Tuple[str, str]) -> str:
        suffix = variants[0] if self._is_hard(word) else variants[1]
        return word + (suffix.upper() if word.isupper() and len(word) > 1 else suffix)

    def inflect(self, name: Optional[str], case: str) -> Optional[str]:
        """Склоняет имя, ФИО или местоимение. Неизвестный падеж: слово как есть или ValueError в strict."""
        if name is None:
            return None
        word = name.strip()
        case_lower = case.lower()
        if not word or case_lower == 'nominative':
            return word

        pronoun = self._PRONOUNS.get(word.lower())
        if pronoun is not None:
            form = pronoun.get(case_lower)
            if form is None:
                return self._unknown(word, f'case {case!r}')
            return form.capitalize() if word[0].isupper() else form

        if ' ' in word:
            return ' '.join(
                part if part.lower().endswith(self._PATRONYMIC_SUFFIXES) else self.inflect(part, case_lower)
                for part in word.split()
            )

        if '-' in word:
            head, _, tail = word.rpartition('-')
            return f'{head}-{self.inflect(tail, case_lower)}'

        return self._inflect_word(word, case_lower)

    def _inflect_word(self, word: str, case: str) -> str:
        suffixes = self._CASE_SUFFIXES.get(case)
        if suffixes is None:
            return self._unknown(word, f'case {case!r}')
        return self._add_suffix(word, suffixes[self._ending_class(word)])

    def possessive(self, name: str, person: str = '3', case: str = 'nominative', plural: bool = False) -> str:
        """
        Притяжательная форма с падежом: possessive('Арна', '1sg', 'dative') → 'Арнама'.

        person: '1sg' (менің), '2sg' (сенің), '2sg_formal' (сіздің), '1pl' (біздің),
        '2pl' (сендердің), '2pl_formal' (сіздердің), '3' (оның/олардың).
        plural=True — несколько обладаемых: Арналарым, Нұрландары.
        В ФИО форму принимает только последняя часть.
        """
        word = name.strip()
        case_lower = case.lower()
        # 2-е лицо мн. ч. владельца = -лар/-лер + суффикс 2-го лица ед. ч.: үйлерің, үйлеріңіз
        owner_plural = person in ('2pl', '2pl_formal')
        base_person = {'2pl': '2sg', '2pl_formal': '2sg_formal'}.get(person, person)
        variants = self._POSSESSIVE_SUFFIXES.get(base_person)
        if not word:
            return word
        if variants is None:
            return self._unknown(word, f'person {person!r}')

        if ' ' in word or '-' in word:
            sep = ' ' if ' ' in word else '-'
            head, _, tail = word.rpartition(sep)
            return f'{head}{sep}{self.possessive(tail, person, case_lower, plural)}'

        if plural or owner_plural:
            word = self.pluralize(word)

        if self._ending_class(word) == 'vowel':
            base = self._add_suffix(word, variants[0])
        else:
            base = self._add_suffix(self._voice(word), variants[1])
        if case_lower == 'nominative':
            return base

        if base_person == '3':
            suffixes = self._PRONOMINAL_CASE_SUFFIXES.get(case_lower)
            return self._unknown(base, f'case {case!r}') if suffixes is None else self._add_suffix(base, suffixes)
        # После притяжательных -м/-ң барыс септік теряет начальный согласный: Арнама, Арнаңа
        if case_lower == 'dative' and base_person in ('1sg', '2sg'):
            return self._add_suffix(base, ('а', 'е'))
        return self._inflect_word(base, case_lower)

    def genitive_phrase(self, owner: str, thing: str, case: str = 'nominative', plural: bool = False) -> str:
        """
        Изафет «чей-то что-то»: genitive_phrase('Нұрлан', 'әке') → 'Нұрланның әкесі'.
        Местоимение-владелец задаёт лицо: genitive_phrase('мен', 'кітап') → 'менің кітабым'.
        """
        owner_word = owner.strip()
        person = self._PRONOUN_PERSONS.get(owner_word.lower(), '3')
        return f"{self.inflect(owner_word, 'genitive')} {self.possessive(thing, person, case, plural)}"

    def predicate(self, word: str, person: str) -> str:
        """
        Сказуемое с личным окончанием: predicate('студент', '1sg') → 'студентпін'.

        person: '1sg' (мен), '2sg' (сен), '2sg_formal' (сіз), '1pl' (біз),
        '2pl' (сендер), '2pl_formal' (сіздер), '3' (ол/олар — без окончания).
        """
        stripped = word.strip()
        variants = self._PREDICATE_SUFFIXES.get(person)
        if not stripped:
            return stripped
        if variants is None:
            return self._unknown(stripped, f'person {person!r}')
        ending = self._ending_class(stripped)
        index = 1 if ending == 'voiced' else 2 if ending == 'voiceless' else 0
        return self._add_suffix(stripped, variants[index])

    def _voice(self, word: str) -> str:
        return word[:-1] + self._VOICING.get(word[-1], word[-1])

    def _unknown(self, word: str, what: str) -> str:
        if self.strict:
            raise ValueError(f'Unknown {what}')
        return word

    def pluralize(self, name: str) -> str:
        """Возвращает множественное число: -лар/-лер, -дар/-дер или -тар/-тер."""
        word = name.strip()
        if not word:
            return word
        if word[-1].lower() == 'л':
            return self._add_suffix(word, ('дар', 'дер'))
        return self._add_suffix(word, self._PLURAL_SUFFIXES[self._ending_class(word)])

    def declension(self, name: str) -> Dict[str, Tuple[str, str]]:
        """Возвращает все падежи для имени в форме {падеж: (ед. ч., мн. ч.)}."""
        plural = self.pluralize(name)
        return {case: (self.inflect(name, case), self.inflect(plural, case)) for case in self.CASES}
