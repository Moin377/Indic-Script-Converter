from indictrans import Transliterator

MODELS = {
    # Hindustani languages
    ('hi-IN', 'ur-PK'): Transliterator(source='hin', target='urd', build_lookup=True, rb=False),
    ('ur-PK', 'hi-IN'): Transliterator(source='urd', target='hin', build_lookup=True, rb=False),

    # 🌟 Gujarati ↔ Urdu
    ('gu-IN', 'ur-PK'): Transliterator(source='guj', target='urd', build_lookup=True, rb=False),
    ('ur-PK', 'gu-IN'): Transliterator(source='urd', target='guj', build_lookup=True, rb=False),
}

def ml_transliterate(text: str, from_script: str, to_script: str) -> str:
    """
    Machine-Learning-based Transliteration for the given `text` between required scripts.

    Args:
        text (str): Text to be converted
        from_script (str): Source script (e.g., 'gu-IN', 'ur-PK')
        to_script (str): Target script (e.g., 'ur-PK', 'gu-IN')

    Returns:
        str: Transliterated text by models
    """
    if (from_script, to_script) not in MODELS:
        raise ValueError(f"Unsupported conversion from {from_script} to {to_script}")

    return MODELS[(from_script, to_script)].transform(text)
