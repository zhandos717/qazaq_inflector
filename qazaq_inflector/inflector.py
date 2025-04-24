from typing import Optional, Dict, Union


class QazaqNameInflector:
    """
    Инфлектор казахских имён, ФИО и местоимений: добавляет суффиксы падежей согласно гармонии гласных,
    типу последнего согласного и фонетическим правилам.

    Поддерживаемые падежи:
      - nominative      — именительный
      - genitive       — родительный
      - dative         — дательный
      - accusative     — винительный
      - locative       — местный
      - ablative       — исходный
      - instrumental    — творительный

    Особенности:
      - ФИО: части, оканчивающиеся на 'ұлы' или 'қызы', не склоняются.
      - Слова через пробел или дефис обрабатываются по частям.
      - Местоимения (мен, біз, сен, сіз, ол) имеют специальные формы.
    """

    # Гласные и согласные группы
    _HARD_VOWELS = {'а', 'ұ', 'ы', 'о'}
    _SOFT_VOWELS = {'ә', 'ү', 'і', 'ө', 'е', 'э'}
    _SIBILANTS = {'к', 'қ', 'п', 'с', 'т', 'ш', 'ч', 'ц'}
    _PATRONYMIC_SUFFIXES = ('ұлы', 'қызы')

    # Личные местоимения
    _PRONOUNS: Dict[str, Dict[str, str]] = {
        'мен': {
            'nominative': 'мен',  'genitive': 'менің',   'dative': 'маған',  'accusative': 'мені',
            'locative':   'менде', 'ablative': 'меннен', 'instrumental': 'менімен'
        },
        'біз': {
            'nominative': 'біз',  'genitive': 'біздің',  'dative': 'бізге',  'accusative': 'бізді',
            'locative':   'бізде', 'ablative': 'бізден', 'instrumental': 'бізбен'
        },
        'сен': {
            'nominative': 'сен',  'genitive': 'сенің',   'dative': 'саған',  'accusative': 'сені',
            'locative':   'сенде', 'ablative': 'сеннен', 'instrumental': 'сенмен'
        },
        'сіз': {
            'nominative': 'сіз',  'genitive': 'сіздің',  'dative': 'сізге',  'accusative': 'сізді',
            'locative':   'сізде', 'ablative': 'сізден', 'instrumental': 'сізбен'
        },
        'ол': {
            'nominative': 'ол',   'genitive': 'оның',    'dative': 'оған',   'accusative': 'оны',
            'locative':   'онда',  'ablative': 'одан',   'instrumental': 'онымен'
        }
    }

    # Суффиксы для имён по падежам
    _CASE_SUFFIXES: Dict[str, Dict[str, Union[str, Dict[str, str]]]] = {
        'genitive': {
            'hard': 'дың', 'soft': 'дің',
            'sibilant': {'hard': 'тың', 'soft': 'тің'},
            'n_ending': {'hard': 'ның', 'soft': 'нің'}
        },
        'dative': {
            'hard': 'ға', 'soft': 'ге',
            'sibilant': {'hard': 'қа', 'soft': 'ке'},
            'n_ending': {'hard': 'ға', 'soft': 'ге'}
        },
        'accusative': {
            'hard': 'ды', 'soft': 'ді',
            'sibilant': {'hard': 'ты', 'soft': 'ті'},
            'n_ending': {'hard': 'ды', 'soft': 'ді'}
        },
        'locative': {
            'hard': 'да', 'soft': 'де',
            'sibilant': {'hard': 'та', 'soft': 'те'},
            'n_ending': {'hard': 'нда', 'soft': 'нде'}
        },
        'ablative': {
            'hard': 'дан', 'soft': 'ден',
            'sibilant': {'hard': 'тан', 'soft': 'тен'},
            'n_ending': {'hard': 'дан', 'soft': 'ден'}
        },
        'instrumental': {
            'hard': 'мен', 'soft': 'мен',
            'sibilant': 'пен', 'n_ending': 'мен'
        }
    }

    def _get_vowel_harmony(self, word: str) -> str:
        """Определяет последнюю по тексту гармонию гласного: 'hard' или 'soft'."""
        for ch in reversed(word.lower()):
            if ch in self._HARD_VOWELS:
                return 'hard'
            if ch in self._SOFT_VOWELS:
                return 'soft'
        return 'hard'

    def _get_last_consonant_type(self, word: str) -> Optional[str]:
        """Определяет тип последнего согласного: 'n_ending' или 'sibilant'."""
        last = word[-1].lower()
        if last in {'н', 'ң'}:
            return 'n_ending'
        if last in self._SIBILANTS:
            return 'sibilant'
        return None

    def inflect(self, name: Optional[str], case: str) -> Optional[str]:
        """Склоняет имя или слово по падежу."""
        if name is None:
            return None
        word = name.strip()
        case_lower = case.lower()
        if not word or case_lower == 'nominative':
            return word

        # Местоимения
        pron = word.lower()
        if pron in self._PRONOUNS:
            form = self._PRONOUNS[pron].get(case_lower)
            return form.capitalize() if word[0].isupper() else form

        # ФИО через пробел
        if ' ' in word:
            parts = []
            for part in word.split():
                if any(part.lower().endswith(suf) for suf in self._PATRONYMIC_SUFFIXES):
                    parts.append(part)
                else:
                    parts.append(self.inflect(part, case_lower))
            return ' '.join(parts)

        # Слова через дефис
        if '-' in word:
            return '-'.join(self.inflect(sub, case_lower) for sub in word.split('-'))

        # Стандартное склонение для имён
        suffix_map = self._CASE_SUFFIXES.get(case_lower)
        if not suffix_map:
            return word
        harmony = self._get_vowel_harmony(word)
        ctype   = self._get_last_consonant_type(word)
        # приоритет: окончание по последней букве, затем гармония
        rule    = suffix_map.get(ctype) or suffix_map.get(harmony)
        if isinstance(rule, dict):
            suffix = rule[harmony]
        else:
            suffix = rule
        return word + suffix

    def pluralize(self, name: str) -> str:
        """Возвращает множественное число: добавляет '-дар' или '-дер'."""
        harmony = self._get_vowel_harmony(name)
        return name + ('дар' if harmony == 'hard' else 'дер')

    def declension(self, name: str) -> Dict[str, tuple]:
        """Возвращает все падежи для имени в форме (ед., мн.)."""
        result: Dict[str, tuple] = {}
        for case in ['nominative','genitive','dative','accusative','locative','ablative','instrumental']:
            singular = self.inflect(name, case)
            plural   = self.inflect(self.pluralize(name), case)
            result[case] = (singular, plural)
        return result
