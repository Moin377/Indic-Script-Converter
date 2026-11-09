import re
from .str_mapper import StringTranslator

# -----------------------------
# Existing Preprocessing Mappings
# -----------------------------

DEVANAGARI_PREPROCESS_MAP = {
    # Desanskritize
    'ँ': 'ं',
    'ऋ': 'र',
    'ॠ': 'र',
    'ऌ': 'ल',
    'ॡ': 'ल',
    'ृ': '्र',
    'ॄ': '्र',
    'ॢ': '्ल',
    'ॣ': '्ल',

    # Dekashmirize
    'ऄ': 'अ',
    'ऎ': 'ए',
    'ऒ': 'ओ',
    'ॆ': 'े',
    'ॊ': 'ो',

    # Delatinize
    'ॲ': 'अ',
    'ऑ': 'आ',
    'ऍ': 'ए',
    'ॅ': '',
    'ॉ': 'ा',

    # Dedravidize
    'ऩ': 'न',
    'ऱ': 'र',
    'ल़': 'ल',
    'ऴ': 'ळ',

    # De-bangalize
    'य़': 'य',
    'व़': 'व',  # W->V

    # Misc
    'थ़': 'थ',
    'म़': 'म',
    '॰': '.',
}
devanagari_preprocessor = StringTranslator(DEVANAGARI_PREPROCESS_MAP)

DEVANAGARI_SHORT_VOWELS_REMOVE_MAP = {
    # Abjadi-purifier
    'ि': '',
    'ु': '',
}
devanagari_short_vowels_remover = str.maketrans(DEVANAGARI_SHORT_VOWELS_REMOVE_MAP)

DEVANAGARI_NON_INITIAL_VOWELS_ABJADIFY = {
    'ै': 'े',
    'ौ': 'ो',
    'ू': 'ो',

    # Handle non-initial vowels missing in sheet
    'उ': 'ओ',
    'ऊ': 'ओ',
    'ऐ': 'ए',
    'औ': 'ओ',
}
devanagari_non_initial_vowels_abjadifier = str.maketrans(DEVANAGARI_NON_INITIAL_VOWELS_ABJADIFY)

DEVANAGARI_INITIAL_VOWELS_ABJADIFY = {
    'इ': 'अ',
    'ई': 'ए',
    'उ': 'अ',
    'ऊ': 'ओ',
    'ऐ': 'ए',
    'औ': 'ओ',
}
devanagari_initial_vowels_abjadifier = StringTranslator(DEVANAGARI_INITIAL_VOWELS_ABJADIFY,
                                                       match_initial_only=True,
                                                       support_back_translation=False)

def devanagari_initial_vowels_abjadify(text):
    text = re.sub('((^|[^\u0900-\u0963\u0972-\u097f]))इ', '\\1अ', text)
    text = re.sub('((^|[^\u0900-\u0963\u0972-\u097f]))ई', '\\1ए', text)
    text = re.sub('((^|[^\u0900-\u0963\u0972-\u097f]))उ', '\\1अ', text)
    text = re.sub('((^|[^\u0900-\u0963\u0972-\u097f]))ऊ', '\\1ओ', text)
    text = re.sub('((^|[^\u0900-\u0963\u0972-\u097f]))ऐ', '\\1ए', text)
    text = re.sub('((^|[^\u0900-\u0963\u0972-\u097f]))औ', '\\1ओ', text)
    return text

DEVANAGARI_NUQTA_CONSONANTS_SIMPLIFY_MAP = {
    # Unicode chars
    'क़': 'क',
    'ख़': 'ख',
    'ग़': 'ग',
    # 'ज़': 'ज',
    'ड़': 'ड',
    'ढ़': 'ढ',
    'फ़': 'फ',

    # Constructed chars
    'ज़़': 'ज़',
    'ॹ': 'ज़',
    'ॹ़': 'ज़',
    'त़': 'त',
    'स़': 'स',
    'स़़': 'स',
    'ह़': 'ह',
    'ह॒': 'ह',

    # Implosive to germination (approx)
    'ॻ': 'ग्ग',
    'ॼ': 'ज्ज',
    'ॾ': 'ड्ड',
    'ॿ': 'ब्ब',
}
devanagari_nuqta_consonants_simplifier = StringTranslator(DEVANAGARI_NUQTA_CONSONANTS_SIMPLIFY_MAP,
                                                         support_back_translation=False)

# Unicode keeps the precomposed nukta consonants (eg. \u0958 QA) out of NFC
# (they are composition exclusions), while indicnlp's normalizers decompose them.
# The map files below are written with the precomposed forms, so compose them back.
DEVANAGARI_NUKTA_SIGN = '़'
DEVANAGARI_NUKTA_BASE_LETTERS = 'कखगजडढफय'
DEVANAGARI_NUKTA_PRECOMPOSED_MAP = {base_letter + DEVANAGARI_NUKTA_SIGN: chr(0x0958 + offset)
                                    for offset, base_letter in enumerate(DEVANAGARI_NUKTA_BASE_LETTERS)}


def devanagari_compose_nukta(text):
    for decomposed, precomposed in DEVANAGARI_NUKTA_PRECOMPOSED_MAP.items():
        text = text.replace(decomposed, precomposed)
    return text
