MODELS = {
    # Hindustani languages
    ('hi-IN', 'ur-PK'): {'source': 'hin', 'target': 'urd'},
    ('ur-PK', 'hi-IN'): {'source': 'urd', 'target': 'hin'},

    # Gujarati <-> Urdu
    ('gu-IN', 'ur-PK'): {'source': 'guj', 'target': 'urd'},
    ('ur-PK', 'gu-IN'): {'source': 'urd', 'target': 'guj'},
}

_transliterators = {}


def _get_transliterator(from_script, to_script):
    """
    Build (and cache) the model for the given language pair.

    The models are loaded lazily because indictrans needs to download them on
    first use, which is slow and is not required for the rule-based conversion.
    """
    try:
        model_params = MODELS[(from_script, to_script)]
    except KeyError:
        raise ValueError(f"Unsupported conversion from {from_script} to {to_script}")

    if (from_script, to_script) not in _transliterators:
        from indictrans import Transliterator
        _transliterators[(from_script, to_script)] = Transliterator(build_lookup=True,
                                                                    rb=False,
                                                                    **model_params)
    return _transliterators[(from_script, to_script)]


def ml_transliterate(text: str, from_script: str, to_script: str) -> str:
    """
    Machine-Learning-based Transliteration for the given `text` between required scripts.

    Args:
        text (str): Text to be converted
        from_script (str): Source script (eg. 'hi-IN', 'ur-PK')
        to_script (str): Target script (eg. 'ur-PK', 'gu-IN')

    Returns:
        str: Transliterated text by models
    """
    return _get_transliterator(from_script, to_script).transform(text)
