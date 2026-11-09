from aksharamukha.transliterate import process as aksharamukhi_xlit


def convert_with_diacritics(text: str, from_script: str, to_script: str) -> str:
    """
    Transliterate with diacritics for the given `text` from Indic script to PersoArabic.

    Args:
        text (str): Text to be converted
        from_script (str): Source Indic script (eg. 'hi-IN', 'pa-IN', 'gu-IN')
        to_script (str): Target PersoArabic script (eg. 'ur-PK')

    Returns:
        str: Transliterated text in impure-abjad form
    """
    if from_script == 'hi-IN' and to_script == 'ur-PK':
        # Devanagari (Hindi) -> Shahmukhi
        return aksharamukhi_xlit("Devanagari", "Shahmukhi", text,
                                 pre_options=["RemoveSchwaHindi", "AnuChandraEqDeva"])

    if from_script == 'pa-IN' and to_script == 'pa-PK':
        # Gurmukhi (Punjabi) -> Shahmukhi
        return aksharamukhi_xlit("Gurmukhi", "Shahmukhi", text,
                                 pre_options=["SchwaFinalGurmukhi"])

    if from_script == 'gu-IN' and to_script == 'ur-PK':
        # Gujarati (Gujarati) -> Shahmukhi
        # Gujarati shares the Hindustani phonology (incl. final-schwa deletion),
        # so it is converted to Devanagari first and then to the PersoArabic script.
        devanagari_text = aksharamukhi_xlit("Gujarati", "Devanagari", text)
        return aksharamukhi_xlit("Devanagari", "Shahmukhi", devanagari_text,
                                 pre_options=["RemoveSchwaHindi", "AnuChandraEqDeva"])

    raise ValueError(f"Unsupported conversion from {from_script} to {to_script}")
