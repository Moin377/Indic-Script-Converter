import requests

BASE_URL = "http://sangam.learnpunjabi.org/SindhiTransliteration.asmx/"

ENDPOINTS = {
    # Hindustani languages
    ('hi-IN', 'ur-PK'): BASE_URL + 'Hindi2Urdu',
    ('ur-PK', 'hi-IN'): BASE_URL + 'Urdu2Hindi',

    # Punjabi scripts
    ('pa-IN', 'pa-PK'): BASE_URL + 'Gurmukhi2Shahmukhi',
    ('pa-PK', 'pa-IN'): BASE_URL + 'Shahmukhi2Gurmukhi',

    # Sindhi scripts
    ('sd-IN', 'sd-PK'): BASE_URL + 'SindhiDEV2SindhiUR',
    ('sd-PK', 'sd-IN'): BASE_URL + 'SindhiUR2SindhiDEV',
}

# The SANGAM server does not expose any Gujarati endpoint.
# Gujarati <-> Devanagari is an exact (table-based) script conversion, so Gujarati
# is bridged through Devanagari and the Devanagari endpoints of the server are used.
# Maps (from_script, to_script) -> (devanagari_endpoint_pair, indic_side)
#   'from' : the input is converted Gujarati -> Devanagari before sending
#   'to'   : the response is converted Devanagari -> Gujarati after receiving
GUJARATI_BRIDGED_ENDPOINTS = {
    ('gu-IN', 'ur-PK'): ('from', ('hi-IN', 'ur-PK')),
    ('ur-PK', 'gu-IN'): ('to', ('ur-PK', 'hi-IN')),
}


def _gujarati_to_devanagari(text):
    from .gujarati import convert_gujarati_to_devanagari
    return convert_gujarati_to_devanagari(text)


def _devanagari_to_gujarati(text):
    from .gujarati import convert_devanagari_to_gujarati
    return convert_devanagari_to_gujarati(text)


def _request(api_url, text, retry_attempts):
    for i in range(retry_attempts):
        try:
            response = requests.post(api_url, json={'input': text}, timeout=5)
            return response.json()['d']
        except (requests.exceptions.Timeout, KeyError):
            if i == retry_attempts - 1:
                raise
            continue

    raise requests.exceptions.Timeout("Failed to get response after multiple attempts.")


def online_transliterate(text: str, from_script: str, to_script: str, retry_attempts=5) -> str:
    """
    Transliterate the given `text` between required scripts using SANGAM API.

    Args:
        text (str): Text to be converted
        from_script (str): Source script (eg. 'hi-IN', 'ur-PK')
        to_script (str): Target script (eg. 'ur-PK', 'gu-IN')

    Returns:
        str: Transliterated text from SANGAM server
    """
    if (from_script, to_script) in GUJARATI_BRIDGED_ENDPOINTS:
        indic_side, devanagari_pair = GUJARATI_BRIDGED_ENDPOINTS[(from_script, to_script)]
        if indic_side == 'from':
            text = _gujarati_to_devanagari(text)
        result = _request(ENDPOINTS[devanagari_pair], text, retry_attempts)
        if indic_side == 'to':
            result = _devanagari_to_gujarati(result)
        return result

    try:
        api_url = ENDPOINTS[(from_script, to_script)]
    except KeyError:
        raise ValueError(f"Unsupported conversion from {from_script} to {to_script}")

    return _request(api_url, text, retry_attempts)


# Alias for easier use
convert = online_transliterate

if __name__ == '__main__':
    print(convert('हिन्दुस्तानी', 'hi-IN', 'ur-PK'))
    print(convert('ਹਿੰਦੁਸਤਾਨੀ', 'pa-IN', 'pa-PK'))
    print(convert('सिन्धी', 'sd-IN', 'sd-PK'))
    print(convert('હિન્દુસ્તાની', 'gu-IN', 'ur-PK'))
