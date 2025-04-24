import unittest
from qazaq_inflector import QazaqNameInflector


class TestKazakhNameInflector(unittest.TestCase):
    def setUp(self):
        self.inflector = QazaqNameInflector()

    def test_basic_cases_single_names(self):
        """
        Проверяем все падежи для одиночных имён.
        """
        name = "Нұрлан"
        expected = {
            'nominative': 'Нұрлан',
            'genitive': 'Нұрланның',
            'dative': 'Нұрланға',
            'accusative': 'Нұрланды',
            'locative': 'Нұрланда',
            'ablative': 'Нұрландан',
            'instrumental': 'Нұрланмен',
        }
        for case, exp in expected.items():
            with self.subTest(case=case):
                self.assertEqual(
                    self.inflector.inflect(name, case),
                    exp,
                    f"Падеж {case} для {name}"
                )

    def test_harmony_variations(self):
        """
        Проверка разных сочетаний гласных и типов окончаний.
        """
        data = [
            ("Айгүл", 'genitive', 'Айгүлдің'),
            ("Бақыт", 'dative', 'Бақытқа'),
            ("Аян", 'accusative', 'Аянды'),
            ("Дәулет", 'locative', 'Дәулетте'),
            ("Ерлан", 'ablative', 'Ерландан'),
        ]
        for name, case, exp in data:
            with self.subTest(name=name, case=case):
                self.assertEqual(
                    self.inflector.inflect(name, case),
                    exp
                )

    def test_fio_multiple_parts(self):
        """
        ФИО с пробелом: каждую часть склоняем.
        """
        full = "Абай Құнанбаев"
        self.assertEqual(
            self.inflector.inflect(full, 'dative'),
            'Абайға Құнанбаевге'
        )

    def test_hyphenated_names(self):
        """
        Сложные имена через дефис: склоняем каждую часть.
        """
        hyph = "Гүлнар-Баян"
        self.assertEqual(
            self.inflector.inflect(hyph, 'locative'),
            'Гүлнарда-Баяннда'
        )

    def test_empty_and_none(self):
        """
        Пустая строка и None.
        """
        self.assertEqual(
            self.inflector.inflect("", 'genitive'),
            ""
        )
        self.assertIsNone(
            self.inflector.inflect(None, 'dative')
        )

    def test_invalid_case(self):
        """
        Несуществующий падеж возвращает исходное.
        """
        self.assertEqual(
            self.inflector.inflect("Нұрлан", 'unknown'),
            'Нұрлан'
        )


if __name__ == '__main__':
    unittest.main()
