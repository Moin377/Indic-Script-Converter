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

# -----------------------------
# New: Devanagari to Gujarati Mapping
# -----------------------------

DEVANAGARI_TO_GUJARATI_MAP = {
    # Vowels
    'अ': 'અ', 'आ': 'આ', 'इ': 'ઇ', 'ई': 'ઈ', 'उ': 'ઉ', 'ऊ': 'ઊ',
    'ऋ': 'ઋ', 'ए': 'એ', 'ऐ': 'ઐ', 'ओ': 'ઓ', 'औ': 'ઔ',

    # Diacritic vowels
    'ा': 'ા', 'ि': 'િ', 'ी': 'ી', 'ु': 'ુ', 'ू': 'ૂ', 'ृ': 'ૃ',
    'ॄ': 'ૄ', 'े': 'ે', 'ै': 'ૈ', 'ो': 'ો', 'ौ': 'ૌ',

    # Consonants
    'क': 'ક', 'ख': 'ખ', 'ग': 'ગ', 'घ': 'ઘ', 'ङ': 'ઙ',
    'च': 'ચ', 'छ': 'છ', 'ज': 'જ', 'झ': 'ઝ', 'ञ': 'ઞ',
    'ट': 'ટ', 'ठ': 'ઠ', 'ड': 'ડ', 'ढ': 'ઢ', 'ण': 'ણ',
    'त': 'ત', 'थ': 'થ', 'द': 'દ', 'ध': 'ધ', 'न': 'ન',
    'प': 'પ', 'फ': 'ફ', 'ब': 'બ', 'भ': 'ભ', 'म': 'મ',
    'य': 'ય', 'र': 'ર', 'ल': 'લ', 'व': 'વ', 'श': 'શ',
    'ष': 'ષ', 'स': 'સ', 'ह': 'હ', 'ळ': 'ળ', 'क्ष': 'ક્ષ',
    'त्र': 'ત્ર', 'ज्ञ': 'જ્ઞ',

    # Numbers
    '०': '૦', '१': '૧', '२': '૨', '३': '૩', '४': '૪',
    '५': '૫', '६': '૬', '७': '૭', '८': '૮', '९': '૯',

    # Symbols
    '।': '।', '॥': '॥', 'ं': 'ં', 'ः': 'ઃ', 'ँ': 'ઁ',
    'ॐ': 'ૐ', '।': '।', '।': '।', '।': '।', '।': '।'
}

# Create a translator object for Devanagari to Gujarati
devanagari_to_gujarati_translator = StringTranslator(DEVANAGARI_TO_GUJARATI_MAP)

def convert_devanagari_to_gujarati(text):
    """
    Converts Devanagari script text into Gujarati script.
    """
    return devanagari_to_gujarati_translator.translate(text)

# Optional: Simple Gujarati normalizer
GUJARATI_NORMALIZATION_MAP = {
    'ૅ': '',         # Remove Latin short e variant
    'ૉ': 'ો',        # Normalize to o
    'ૄ': 'ૃ',        # Normalize rare vocalic r variants
    'ૡ': 'ૢ',        # Normalize rare vocalic l variants
    'ઽ': 'હ',        # Replace aspirated h with regular ह
    '૰': '',         # Rare number forms
    '૱': '',         # Rare number forms
    '૲': '',         # Rare number forms
    '૳': '',         # Rare number forms
    '૴': '',         # Rare number forms
    '૵': '',         # Rare number forms
    '૶': '',         # Rare number forms
    '૷': '',         # Rare number forms
    '૸': '',         # Rare number forms
}
gujarati_normalizer = StringTranslator(GUJARATI_NORMALIZATION_MAP)

def normalize_gujarati(text):
    return gujarati_normalizer.translate(text)

# Example usage:
if __name__ == "__main__":
    sample_devanagari = "नमस्ते दुनिया"
    gujarati_text = convert_devanagari_to_gujarati(sample_devanagari)
    print("Gujarati Output:", gujarati_text)
    print("Normalized Gujarati:", normalize_gujarati(gujarati_text))
