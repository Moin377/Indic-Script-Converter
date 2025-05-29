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

    # 🌟 Gujarati scripts
    ('gu-IN', 'gu-PK'): BASE_URL + 'Hindi2Urdu',  # Reuse Hindi→Urdu since it's Devanagari→Arabic
    ('gu-PK', 'gu-IN'): BASE_URL + 'Urdu2Hindi',  # Urdu→Gujarati via Urdu→Devanagari
}

def online_transliterate(text: str, from_script: str, to_script: str, retry_attempts=5) -> str:
    """
    Transliterate the given `text` between required scripts using SANGAM API.

    Args:
        text (str): Text to be converted
        from_script (str): Source script (e.g., 'gu-IN', 'gu-PK')
        to_script (str): Target script (e.g., 'gu-PK', 'gu-IN')

    Returns:
        str: Transliterated text from SANGAM server
    """
    try:
        api_url = ENDPOINTS[(from_script, to_script)]
    except KeyError:
        raise ValueError(f"Unsupported conversion from {from_script} to {to_script}")

    for i in range(retry_attempts):
        try:
            response = requests.post(api_url, json={'input': text}, timeout=5)
            return response.json()['d']
        except (requests.exceptions.Timeout, KeyError):
            if i == retry_attempts - 1:
                raise
            continue

    raise requests.exceptions.Timeout("Failed to get response after multiple attempts.")

# Alias for easier use
convert = online_transliterate

if __name__ == '__main__':
    # Test cases
    print(convert('હિન્દુસ્તાની', 'gu-IN', 'gu-PK'))  # Gujarati → Urdu
    print(convert('હિન્દુસ્તાની', 'gu-PK', 'gu-IN'))  # Urdu → Gujarati

    # Previous tests
    print(convert('हिन्दुस्तानी', 'hi-IN', 'ur-PK'))
    print(convert('ਪੰਜਾਬੀ', 'pa-IN', 'pa-PK'))
    print(convert('सिन्धी', 'sd-IN', 'sd-PK'))
