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
      - Местоимения (мен, біз, сен, сіз, ол) имеют специальные формы.
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

    _PATRONYMIC_SUFFIXES = ('ұлы', 'қызы')
    # Гармонию русских фамилий определяет казахская основа: Құнанбаев → Құнанба-
    _SURNAME_SUFFIXES = ('ова', 'ева', 'ов', 'ев')

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

    _PLURAL_SUFFIXES: Dict[str, Tuple[str, str]] = {
        'vowel': ('лар', 'лер'), 'sonorant': ('лар', 'лер'), 'nasal': ('дар', 'дер'),
        'voiced': ('дар', 'дер'), 'voiceless': ('тар', 'тер'),
    }

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
        """Склоняет имя, ФИО или местоимение по падежу. Неизвестный падеж возвращает слово без изменений."""
        if name is None:
            return None
        word = name.strip()
        case_lower = case.lower()
        if not word or case_lower == 'nominative':
            return word

        pronoun = self._PRONOUNS.get(word.lower())
        if pronoun is not None:
            form = pronoun.get(case_lower, word)
            return form.capitalize() if word[0].isupper() else form

        if ' ' in word:
            return ' '.join(
                part if part.lower().endswith(self._PATRONYMIC_SUFFIXES) else self.inflect(part, case_lower)
                for part in word.split()
            )

        if '-' in word:
            head, _, tail = word.rpartition('-')
            return f'{head}-{self.inflect(tail, case_lower)}'

        suffixes = self._CASE_SUFFIXES.get(case_lower)
        if suffixes is None:
            return word
        return self._add_suffix(word, suffixes[self._ending_class(word)])

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
