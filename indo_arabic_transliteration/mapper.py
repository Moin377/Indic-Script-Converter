from .hindustani import HindustaniTransliterator
hindi_urdu_converter = HindustaniTransliterator()

from .punjabi import PunjabiTransliterator
panjabi_converter = PunjabiTransliterator()

from .sindhi import SindhiTransliterator
sindhi_converter = SindhiTransliterator()

# 🌟 New: Import Gujarati Transliterator
from .gujarati import GujaratiTransliterator
gujarati_converter = GujaratiTransliterator()

# Alternatively, define inline if not imported
# gujarati_converter = GujaratiTransliterator(data_dir='path/to/data')

DELEGATES = {
    # Hindustani languages
    ('hi-IN', 'ur-PK'): hindi_urdu_converter.transliterate_from_hindi_to_urdu,
    ('ur-PK', 'hi-IN'): hindi_urdu_converter.transliterate_from_urdu_to_hindi,
    
    # Punjabi scripts
    ('pa-IN', 'pa-PK'): panjabi_converter.transliterate_from_gurmukhi_to_shahmukhi,
    ('pa-PK', 'pa-IN'): panjabi_converter.transliterate_from_shahmukhi_to_gurmukhi,
    
    # Sindhi scripts
    ('sd-IN', 'sd-PK'): sindhi_converter.transliterate_from_devanagari_to_sindhi,
    ('sd-PK', 'sd-IN'): sindhi_converter.transliterate_from_sindhi_to_devanagari,

    # 🌟 Gujarati to Urdu and vice versa
    ('gu-IN', 'ur-PK'): gujarati_converter.transliterate_from_gujarati_to_urdu,
    ('ur-PK', 'gu-IN'): gujarati_converter.transliterate_from_urdu_to_gujarati,
}

def script_convert(text: str, from_script: str, to_script: str) -> str:
    """
    Raw convert the given `text` between required scripts.

    Args:
        text (str): Text to be converted
        from_script (str): Source script (e.g., 'gu-IN', 'ur-PK')
        to_script (str): Target script (e.g., 'ur-PK', 'gu-IN')

    Returns:
        str: Converted text
    """
    if (from_script, to_script) not in DELEGATES:
        raise ValueError(f"Unsupported conversion from {from_script} to {to_script}")
    
    return DELEGATES[(from_script, to_script)](text)
