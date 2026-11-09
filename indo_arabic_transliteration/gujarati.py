import os
import unicodedata

import pandas as pd
from .hindustani import HindustaniTransliterator
from .str_mapper import StringTranslator

# Gujarati (gu-IN) <=> Perso-Arabic (ur-PK) transliteration.
#
# Gujarati is an Indic script which is nearly isomorphic to Devanagari, so the
# conversion is done in two steps:
#   * Gujarati <-> Devanagari : character-table based (data/gujarati_devanagari.csv)
#   * Devanagari <-> Perso-Arabic : the shared Hindustani rule-based engine
#
# This keeps the Perso-Arabic side of the conversion identical to Hindi-Urdu,
# which is what we want because the Perso-Arabic side of Gujarati is Urdu.

SCRIPT_MAP_FILE = 'gujarati_devanagari.csv'

# Devanagari characters which have no Gujarati counterpart and carry no
# orthographic weight for a Perso-Arabic transliteration. Dropping them keeps
# the Gujarati output free of stray Devanagari (mixed-script) characters.
UNSUPPORTED_DEVANAGARI_CHARS = 'ऺऻॏ॒॑॓॔ॕॖॗॽ'
unsupported_devanagari_remover = str.maketrans('', '', UNSUPPORTED_DEVANAGARI_CHARS)

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def load_script_map(data_dir=DEFAULT_DATA_DIR):
    '''
    Load the Devanagari <-> Gujarati character table.

    The CSV has two rows (one column per character) : the first row holds the
    Devanagari characters and the second row the corresponding Gujarati ones.
    '''
    map_file = os.path.join(data_dir, SCRIPT_MAP_FILE)
    df = pd.read_csv(map_file, header=None, dtype=str, keep_default_na=False)
    if df.shape[0] < 2:
        raise ValueError('Malformed script map file: ' + map_file)

    devanagari_chars, gujarati_chars = list(df.iloc[0]), list(df.iloc[1])
    if len(devanagari_chars) != len(gujarati_chars):
        raise ValueError('Unequal number of columns in the script map file: ' + map_file)

    # The precomposed nukta consonants (eg. \u0958 QA) are composition exclusions, so
    # unicodedata keeps them decomposed. Normalize the column to a single form.
    devanagari_chars = [unicodedata.normalize('NFC', char) for char in devanagari_chars]
    return devanagari_chars, gujarati_chars


def build_script_maps(data_dir=DEFAULT_DATA_DIR):
    '''
    Build the (Devanagari -> Gujarati) and (Gujarati -> Devanagari) maps.

    Several Devanagari letters fall back to the same Gujarati letter (eg. ऎ -> એ),
    so while building the reverse map, the first (canonical) mapping is retained.
    '''
    devanagari_chars, gujarati_chars = load_script_map(data_dir)

    devanagari_to_gujarati_map = dict(zip(devanagari_chars, gujarati_chars))
    gujarati_to_devanagari_map = {}
    for devanagari_char, gujarati_char in zip(devanagari_chars, gujarati_chars):
        gujarati_to_devanagari_map.setdefault(gujarati_char, devanagari_char)
    return devanagari_to_gujarati_map, gujarati_to_devanagari_map


devanagari_to_gujarati_map, gujarati_to_devanagari_map = build_script_maps()
devanagari_to_gujarati_translator = StringTranslator(devanagari_to_gujarati_map,
                                                     support_back_translation=False)
gujarati_to_devanagari_translator = StringTranslator(gujarati_to_devanagari_map,
                                                     support_back_translation=False)


def convert_devanagari_to_gujarati(text):
    '''Convert Devanagari script text into Gujarati script (and drop Devanagari-only marks).'''
    text = text.translate(unsupported_devanagari_remover)
    text = unicodedata.normalize('NFC', text) # Same form as the script map
    return devanagari_to_gujarati_translator.translate(text)


def convert_gujarati_to_devanagari(text):
    '''Convert Gujarati script text into Devanagari script.'''
    return unicodedata.normalize('NFC', gujarati_to_devanagari_translator.translate(text))


class GujaratiTransliterator(HindustaniTransliterator):
    def __init__(self):
        super().__init__()

        from indicnlp.normalize.indic_normalize import GujaratiNormalizer
        self.gujarati_normalizer = GujaratiNormalizer()

    def gujarati_normalize(self, text):
        return self.gujarati_normalizer.normalize(text)

    def devanagari_to_gujarati(self, text):
        return convert_devanagari_to_gujarati(text)

    def gujarati_to_devanagari(self, text):
        text = self.gujarati_normalize(text)
        return convert_gujarati_to_devanagari(text)

    def transliterate_from_gujarati_to_devanagari(self, text):
        return self.gujarati_to_devanagari(text)

    def transliterate_from_devanagari_to_gujarati(self, text):
        return self.devanagari_to_gujarati(text)

    def transliterate_from_gujarati_to_urdu(self, text, nativize=False):
        devanagari_text = self.gujarati_to_devanagari(text)
        return self.transliterate_from_hindi_to_urdu(devanagari_text, nativize=nativize)

    def transliterate_from_urdu_to_gujarati(self, text, nativize=False):
        devanagari_text = self.transliterate_from_urdu_to_hindi(text, nativize=nativize)
        return self.devanagari_to_gujarati(devanagari_text)

    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if src_lang == 'gu' and dest_lang == 'ur':
            return self.transliterate_from_gujarati_to_urdu(text, nativize)
        if src_lang == 'ur' and dest_lang == 'gu':
            return self.transliterate_from_urdu_to_gujarati(text, nativize)
        if src_lang == 'gu' and dest_lang == 'hi':
            return self.transliterate_from_gujarati_to_devanagari(text)
        if src_lang == 'hi' and dest_lang == 'gu':
            return self.transliterate_from_devanagari_to_gujarati(text)
        raise ValueError(f"Unsupported conversion from {src_lang} to {dest_lang}")
