import unittest

from indo_arabic_transliteration.mapper import script_convert


class TestHindustani(unittest.TestCase):
    def test_hindi_to_urdu(self):
        cases = {
            'हैदराबाद': 'ہیدراباد',
            'भारत': 'بھارت',
            'ज़रूर': 'زرور',
            'क़रीब': 'قریب',
            'सड़क': 'سڑک',
        }
        for hindi_text, expected_urdu in cases.items():
            with self.subTest(text=hindi_text):
                self.assertEqual(script_convert(hindi_text, 'hi-IN', 'ur-PK'), expected_urdu)

    def test_urdu_to_hindi(self):
        cases = {
            'حیدرآباد': 'ह़ीदरआबाद',
            'بھارت': 'भारत',
        }
        for urdu_text, expected_hindi in cases.items():
            with self.subTest(text=urdu_text):
                self.assertEqual(script_convert(urdu_text, 'ur-PK', 'hi-IN'), expected_hindi)


class TestPunjabi(unittest.TestCase):
    def test_gurmukhi_to_shahmukhi(self):
        self.assertEqual(script_convert('ਸਿੰਘ', 'pa-IN', 'pa-PK'), 'سںگھ')
        self.assertEqual(script_convert('ਪੰਜਾਬੀ', 'pa-IN', 'pa-PK'), 'پںجابی')

    def test_shahmukhi_to_gurmukhi(self):
        self.assertEqual(script_convert('سنگھ', 'pa-PK', 'pa-IN'), 'ਸਨਘ')


class TestSindhi(unittest.TestCase):
    def test_devanagari_to_sindhi(self):
        cases = {
            'हैदराबाद': 'هیدراباد',
            'सिन्धी': 'سنْڌی',
            'में': 'میں',
            'ड़': 'ڙ',
        }
        for devanagari_text, expected_sindhi in cases.items():
            with self.subTest(text=devanagari_text):
                self.assertEqual(script_convert(devanagari_text, 'sd-IN', 'sd-PK'),
                                 expected_sindhi)

    def test_sindhi_to_devanagari(self):
        self.assertEqual(script_convert('حيدرآباد', 'sd-PK', 'sd-IN'), 'ह़ीदरआबाद')


class TestUnsupportedConversion(unittest.TestCase):
    def test_unknown_pair_raises(self):
        with self.assertRaises(ValueError):
            script_convert('नमस्ते', 'hi-IN', 'sd-PK')


if __name__ == '__main__':
    unittest.main()
