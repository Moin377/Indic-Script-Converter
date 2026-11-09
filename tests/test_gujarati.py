import collections
import glob
import os
import unicodedata
import unittest

import pandas as pd

from indo_arabic_transliteration.common import DEVANAGARI_PREPROCESS_MAP
from indo_arabic_transliteration.gujarati import (UNSUPPORTED_DEVANAGARI_CHARS,
                                                  convert_devanagari_to_gujarati,
                                                  convert_gujarati_to_devanagari,
                                                  load_script_map)
from indo_arabic_transliteration.lossless_converter import convert_with_diacritics
from indo_arabic_transliteration.mapper import script_convert

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'indo_arabic_transliteration', 'data')

DEVANAGARI_RANGE = range(0x0900, 0x0980)
GUJARATI_RANGE = range(0x0A80, 0x0B00)


def nfc(text):
    '''Nukta consonants (eg. \u0958 QA) are composition exclusions, so compare in NFC.'''
    return unicodedata.normalize('NFC', text)


def devanagari_chars_in(text):
    return [c for c in text if ord(c) in DEVANAGARI_RANGE]


def gujarati_chars_in(text):
    return [c for c in text if ord(c) in GUJARATI_RANGE]


class TestGujaratiToUrdu(unittest.TestCase):
    def test_common_words(self):
        cases = {
            'ગુજરાત': 'گجرات',
            'ભારત': 'بھارت',
            'ગુજરાતી': 'گجراتی',
            'પાણી': 'پاݨی',
            'છોકરો': 'چھوکرو',
            'હૈદરાબાદ': 'ہیدراباد',
            'નમસ્તે દુનિયા': 'نمسْتے دنیا',
        }
        for gujarati_text, expected_urdu in cases.items():
            with self.subTest(text=gujarati_text):
                self.assertEqual(script_convert(gujarati_text, 'gu-IN', 'ur-PK'), expected_urdu)

    def test_nukta_consonants(self):
        # જ઼ -> ज़ -> ز and ક઼ -> क़ -> ق
        self.assertEqual(script_convert('જ઼રૂર', 'gu-IN', 'ur-PK'), 'زرور')
        self.assertEqual(script_convert('ક઼રીબ', 'gu-IN', 'ur-PK'), 'قریب')

    def test_numerals(self):
        self.assertEqual(script_convert('૧૨૩', 'gu-IN', 'ur-PK'), '۱۲۳')

    def test_no_gujarati_left_in_output(self):
        for text in ['ગુજરાતી ભાષા', 'નમસ્તે દુનિયા', 'કેમ છો']:
            with self.subTest(text=text):
                self.assertEqual(gujarati_chars_in(script_convert(text, 'gu-IN', 'ur-PK')), [])


class TestUrduToGujarati(unittest.TestCase):
    def test_common_words(self):
        cases = {
            'بھارت': 'ભારત',
            'پانی': 'પાની',
            'کتاب': 'કતાબ',
            'پاکستان': 'પાકસતાન',
            'ٹھیک ہے': 'ઠીક હે',
        }
        for urdu_text, expected_gujarati in cases.items():
            with self.subTest(text=urdu_text):
                self.assertEqual(script_convert(urdu_text, 'ur-PK', 'gu-IN'), expected_gujarati)

    def test_no_devanagari_left_in_output(self):
        # Urdu -> Gujarati goes through Devanagari, so no Devanagari may survive
        # in the output (no mixed-script text)
        for text in ['حیدرآباد', 'خوبصورت', 'آپ کیسے ہیں', 'اردو زبان', 'ضرور']:
            with self.subTest(text=text):
                converted = script_convert(text, 'ur-PK', 'gu-IN')
                self.assertEqual(devanagari_chars_in(converted), [])


class TestGujaratiDevanagariScriptConversion(unittest.TestCase):
    def test_gujarati_to_devanagari(self):
        cases = {
            'નમસ્તે': 'नमस्ते',
            'વિદ્યાર્થી': 'विद्यार्थी',
            'ક્ષેત્ર': 'क्षेत्र',
            'જ઼રૂર': 'ज़रूर',
            'શ્રી': 'श्री',
            'ૐ': 'ॐ',
            '૧૨૩': '१२३',
        }
        for gujarati_text, expected_devanagari in cases.items():
            with self.subTest(text=gujarati_text):
                self.assertEqual(script_convert(gujarati_text, 'gu-IN', 'hi-IN'),
                                 nfc(expected_devanagari))

    def test_devanagari_to_gujarati(self):
        cases = {
            'नमस्ते': 'નમસ્તે',
            'विद्यार्थी': 'વિદ્યાર્થી',
            'क्षेत्र': 'ક્ષેત્ર',
            'ज़रूर': 'જ઼રૂર',
            'श्री': 'શ્રી',
            'ॐ': 'ૐ',
            'हिन्दुस्तान': 'હિન્દુસ્તાન',
            '१२३': '૧૨૩',
        }
        for devanagari_text, expected_gujarati in cases.items():
            with self.subTest(text=devanagari_text):
                self.assertEqual(script_convert(devanagari_text, 'hi-IN', 'gu-IN'),
                                 expected_gujarati)

    def test_round_trip(self):
        words = ['नमस्ते', 'भारत', 'क्षेत्र', 'ज़रूर', 'श्री', 'विद्यार्थी',
                 'ॐ', '१२३', 'हिन्दुस्तान', 'पुस्तक', 'सड़क', 'अंदाज़', 'हिंदी']
        for word in words:
            with self.subTest(word=word):
                gujarati_text = convert_devanagari_to_gujarati(word)
                self.assertEqual(nfc(convert_gujarati_to_devanagari(gujarati_text)), nfc(word))

    def test_unsupported_devanagari_marks_are_dropped(self):
        # Devanagari-only (vedic) marks have no Gujarati counterpart
        self.assertEqual(convert_devanagari_to_gujarati('क़॑'), 'ક઼')


class TestLosslessConversion(unittest.TestCase):
    def test_gujarati_to_shahmukhi_with_diacritics(self):
        self.assertEqual(convert_with_diacritics('ગુજરાત', 'gu-IN', 'ur-PK'), 'گُجْرَاتْ')

    def test_same_as_the_hindi_path(self):
        # Gujarati and Hindi share the Hindustani phonology, so the PersoArabic
        # output must be the same for the same word
        self.assertEqual(convert_with_diacritics('ગુજરાતી ભાષા', 'gu-IN', 'ur-PK'),
                         convert_with_diacritics('गुजराती भाषा', 'hi-IN', 'ur-PK'))

    def test_unsupported_pair(self):
        with self.assertRaises(ValueError):
            convert_with_diacritics('ગુજરાત', 'gu-IN', 'sd-PK')


class TestScriptMapData(unittest.TestCase):
    def test_every_devanagari_character_of_the_maps_has_a_gujarati_mapping(self):
        '''Every Devanagari character produced by the shared maps must be convertible.'''
        devanagari_to_gujarati_map = dict(zip(*load_script_map(DATA_DIR)))
        allowed_as_is = set('।॥\u200c\u200d') | set(UNSUPPORTED_DEVANAGARI_CHARS)

        for character in self._devanagari_characters_of_the_shared_maps():
            with self.subTest(character=character):
                self.assertTrue(character in devanagari_to_gujarati_map or character in allowed_as_is,
                                f'No Gujarati mapping for {character!r}')

    def test_unambiguous_characters_are_reversible(self):
        devanagari_chars, gujarati_chars = load_script_map(DATA_DIR)
        occurrences = collections.Counter(gujarati_chars)

        for devanagari_char, gujarati_char in zip(devanagari_chars, gujarati_chars):
            if occurrences[gujarati_char] != 1:
                continue # Many-to-one mappings (eg. ऎ -> એ) can't be reversed
            with self.subTest(character=devanagari_char):
                self.assertEqual(convert_devanagari_to_gujarati(devanagari_char), gujarati_char)
                self.assertEqual(convert_gujarati_to_devanagari(gujarati_char), devanagari_char)

    @staticmethod
    def _devanagari_characters_of_the_shared_maps():
        characters = set()
        for map_file in glob.glob(os.path.join(DATA_DIR, '*.csv')):
            if 'gujarati' in os.path.basename(map_file):
                continue
            df = pd.read_csv(map_file, header=None, dtype=str, keep_default_na=False)
            for value in df.iloc[-1]:
                characters.update(c for c in nfc(value) if ord(c) in DEVANAGARI_RANGE)

        for key, value in DEVANAGARI_PREPROCESS_MAP.items():
            characters.update(c for c in nfc(key + value) if ord(c) in DEVANAGARI_RANGE)
        return characters


if __name__ == '__main__':
    unittest.main()
