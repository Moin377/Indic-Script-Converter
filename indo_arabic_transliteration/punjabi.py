from .hindustani import HindustaniTransliterator

class PunjabiTransliterator(HindustaniTransliterator):
    def __init__(self):
        super().__init__()

        from indicnlp.normalize.indic_normalize import GurmukhiNormalizer
        self.gurmukhi_normalizer = GurmukhiNormalizer()

        from aksharamukha.transliterate import process
        self.aksharamukha_xlit = process

    def transliterate_from_gurmukhi_to_shahmukhi(self, text):
        text = self.gurmukhi_normalizer.normalize(text)
        text = self.aksharamukha_xlit("Gurmukhi", "Devanagari", text)
        return self.transliterate_from_hindi_to_urdu(text)

    def transliterate_from_shahmukhi_to_gurmukhi(self, text):
        text = self.transliterate_from_urdu_to_hindi(text)
        return self.aksharamukha_xlit("Devanagari", "Gurmukhi", text)

    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if src_lang == 'pa' and dest_lang == 'pnb':
            return self.transliterate_from_gurmukhi_to_shahmukhi(text)
        else:
            return self.transliterate_from_shahmukhi_to_gurmukhi(text)


# -----------------------------
# 🌟 New: Gujarati Transliterator
# -----------------------------

class GujaratiTransliterator(HindustaniTransliterator):
    def __init__(self):
        super().__init__()

        from indicnlp.normalize.indic_normalize import DevanagariNormalizer
        self.gujarati_normalizer = DevanagariNormalizer()

        from aksharamukha.transliterate import process
        self.aksharamukha_xlit = process

    def transliterate_from_gujarati_to_urdu(self, text):
        """Convert Gujarati script text to Urdu-Arabic"""
        text = self.gujarati_normalizer.normalize(text)
        # First convert Gujarati → Devanagari (if needed)
        dev_text = self.aksharamukha_xlit("Gujarati", "Devanagari", text)
        # Then Devanagari → Urdu
        return self.transliterate_from_hindi_to_urdu(dev_text)

    def transliterate_from_urdu_to_gujarati(self, text):
        """Convert Urdu-Arabic script text to Gujarati"""
        # First convert Urdu → Devanagari
        dev_text = self.transliterate_from_urdu_to_hindi(text)
        # Then Devanagari → Gujarati
        return self.aksharamukha_xlit("Devanagari", "Gujarati", dev_text)

    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if src_lang == 'gu' and dest_lang == 'ur':
            return self.transliterate_from_gujarati_to_urdu(text)
        elif src_lang == 'ur' and dest_lang == 'gu':
            return self.transliterate_from_urdu_to_gujarati(text)
        else:
            raise ValueError(f"Unsupported conversion from {src_lang} to {dest_lang}")
