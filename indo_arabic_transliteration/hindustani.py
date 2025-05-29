from .base import BaseIndoArabicTransliterator
from .common import convert_devanagari_to_gujarati, normalize_gujarati
import re

URDU_POSTPROCESS_MAP = {
    # Normalizer to modern Urdu
    'ݨ': "ن",
    'ࣇ': "ل",
}
urdu_postprocessor = str.maketrans(URDU_POSTPROCESS_MAP)

CONSONANT_MAP_FILES = ['hindustani_consonants.csv']

class HindustaniTransliterator(BaseIndoArabicTransliterator):
    def __init__(self):
        super().__init__(CONSONANT_MAP_FILES)
        
        # Monkey patch: Force ह to map only to Urdu ہ (not ھ)
        self.arabic_to_devanagari_converter_pass2.reverse_translation_dict['ह'] = 'ہ'
        self.arabic_to_devanagari_converter_pass2.reverse_translation_dict['ह'+'ा'] = 'ہ'+'ا'
        self.arabic_to_devanagari_converter_pass1.reverse_translation_dict['ह्ह'] = 'ہّ'
        self.arabic_to_devanagari_converter_pass1.reverse_translation_dict['ह्ह'+'ा'] = 'ہّ'+'ا'
    
    def transliterate_ambiguous_urdu_words_to_hindi(self, text):
        # TODO: Handle these using mapper
        text = re.sub(r"(\b)و(\b)", "\\1व\\2", text)
        text = re.sub(r"(\b)کیں(\b)", "\\1कीं\\2", text)
        text = re.sub(r"(\b)نہیں(\b)", "\\1नहीं\\2", text)
        return text
    
    def transliterate_from_urdu_to_hindi(self, text, nativize=False):
        text = self.arabic_normalize(text)
        text = self.transliterate_ambiguous_urdu_words_to_hindi(text)
        text = self.initial_arabic_to_devanagari_converter.translate(text)
        
        # Convert Hamza-combos first, then remaining hamza
        text = self.hamza_combo_to_devanagari_converter.translate(text)
        text = self.hamza_to_devanagari_converter.translate(text)
        
        text = self.arabic_to_devanagari_converter_pass1.translate(text)
        text = self.final_arabic_to_devanagari_converter.translate(text)
        text = self.arabic_to_devanagari_converter_pass2.translate(text)
        text = self.arabic_to_devanagari_final_cleanup.translate(text)
        text = self.devanagari_postprocessor.translate(text) #  (جمہوریہ) जमहवरयह -> जमहोरयह
        text = self.devanagari_postprocessor.translate(text) # जमहोरयह -> जमहोरीह
        if nativize:
            text = self.devanagari_nativize(text)
        return text

    def transliterate_from_hindi_to_urdu(self, text, nativize=False):
        text = self.devanagari_normalize(text)
        text = re.sub('((^|[^\u0900-\u0963\u0972-\u097f]))ए', '\\1ای', text) # Patch: ए is present in both hamza and initial vowels, so handle first

        # Convert Devanagari-Hamza first, then hamza-combos
        text = self.hamza_to_devanagari_converter.reverse_translate(text)
        text = self.hamza_combo_to_devanagari_converter.reverse_translate(text)

        text = self.arabic_to_devanagari_converter_pass1.reverse_translate(text)
        text = self.devanagari_remove_short_vowels(text) # Running it now since previous pass could have handled some short vowels (hamza_combos)
        text = text.replace('ा', 'ا') # Regex finds 'ा' as a \b unfortunately. So a quick hack to avoid those confusions
        text = self.final_arabic_to_devanagari_converter.reverse_translate(text)
        text = text.replace('ी', 'ی').replace('ो', 'و').replace('े', 'ے') # In-case anything remains, should never happen tho
        text = self.initial_arabic_to_devanagari_converter.reverse_translate(text)
        text = text.replace("ओ", "ؤ")
        text = self.arabic_to_devanagari_converter_pass2.reverse_translate(text)
        text = self.arabic_to_devanagari_final_cleanup.reverse_translate(text)
        
        if nativize:
            text = text.translate(urdu_postprocessor)
        return text
    
    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if dest_lang == 'ur':
            return self.transliterate_from_hindi_to_urdu(text, nativize)
        return self.transliterate_from_urdu_to_hindi(text, nativize)


# -------------------------------------------
# 🌟 New Class: Gujarati Transliterator
# -------------------------------------------

class GujaratiTransliterator(BaseIndoArabicTransliterator):
    def __init__(self, data_dir=None):
        super().__init__(
            consonants_map_files=['gujarati/consonants.csv'],
            data_dir=data_dir
        )
        # Load Gujarati-specific postprocessing rules
        gujarati_postprocess_map_file = os.path.join(self.data_dir, 'gujarati/postprocess.csv')
        df = pd.read_csv(gujarati_postprocess_map_file, header=None)
        for i in df.columns:
            src, tgt = str(df[i][0]).strip(), str(df[i][1]).strip()
            self.devanagari_postprocess_map[src] = tgt
        self.devanagari_postprocessor = StringTranslator(self.devanagari_postprocess_map)

    def transliterate_from_urdu_to_gujarati(self, text, nativize=False):
        """Convert Urdu-Arabic script to Gujarati via Devanagari"""
        dev_text = super().transliterate_from_urdu_to_hindi(text, nativize=nativize)
        guj_text = convert_devanagari_to_gujarati(dev_text)
        guj_text = normalize_gujarati(guj_text)
        return guj_text

    def transliterate_from_gujarati_to_urdu(self, text, nativize=False):
        """Convert Gujarati script back to Urdu-Arabic"""
        # First convert Gujarati → Devanagari
        from indicnlp.transliterate.unicode_transliterate import UnicodeIndicTransliterator
        dev_text = UnicodeIndicTransliterator.transliterate(text, 'gu', 'hi')

        # Then Devanagari → Urdu
        urdu_text = super().transliterate_from_hindi_to_urdu(dev_text, nativize=nativize)
        return urdu_text

    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if dest_lang == 'gu':
            return self.transliterate_from_urdu_to_gujarati(text, nativize)
        elif dest_lang == 'ur':
            return self.transliterate_from_gujarati_to_urdu(text, nativize)
        else:
            raise ValueError(f"Unsupported destination language: {dest_lang}")
