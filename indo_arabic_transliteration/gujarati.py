from .base import BaseIndoArabicTransliterator
from .str_mapper import StringTranslator # Though not used initially, good to have for future
import re

# GUJARATI_PREPROCESS_MAP = {} # Example: for pre-processing rules
# gujarati_preprocessor = StringTranslator(GUJARATI_PREPROCESS_MAP)

# GUJARATI_POSTPROCESS_MAP = {} # Example: for post-processing rules
# gujarati_postprocessor = str.maketrans(GUJARATI_POSTPROCESS_MAP)

CONSONANT_MAP_FILES = ['gujarati_consonants.csv']

class GujaratiTransliterator(BaseIndoArabicTransliterator):
    def __init__(self):
        super().__init__(CONSONANT_MAP_FILES)
        # Add any Gujarati-specific initializations here if needed in the future
        # For example, loading additional map files for isolated characters or special forms
        # self.isolated_gujarati_to_devanagari_map = {}
        # self.isolated_gujarati_to_devanagari_converter = StringTranslator(self.isolated_gujarati_to_devanagari_map)

    def arabic_normalize(self, text):
        # For Gujarati (which is not an Arabic script), this might translate to "gujarati_normalize_perso_arabic_input"
        # Or, more likely, this method will be less relevant if direct Gujarati script input is assumed.
        # For now, let's assume it calls the base normalizer which might handle common characters.
        text = super().arabic_normalize(text)
        # Add any Gujarati-specific normalization for Perso-Arabic script input if ever needed
        # text = gujarati_preprocessor.translate(text) # Example
        return text

    def devanagari_normalize(self, text, abjadify_initial_vowels=False, drop_virama=False):
        text = super().devanagari_normalize(text, abjadify_initial_vowels, drop_virama)
        # Add any Gujarati-specific normalization for Devanagari script input if needed
        return text

    def transliterate_from_gujarati_to_devanagari(self, text, nativize=False):
        # Since Gujarati script is the source, we'll use 'arabic_normalize' as a stand-in for 'source_script_normalize'
        # This assumes the input 'text' is in Gujarati script.
        # The base class methods like initial_arabic_to_devanagari_converter assume Perso-Arabic input.
        # We need to ensure our gujarati_consonants.csv is used effectively.
        
        # Step 1: (If any) Gujarati specific pre-processing before applying base transliteration rules.
        # text = gujarati_preprocessor.translate(text) # if you have specific gujarati string replacements

        # The core transliteration will be handled by the base class's mappers
        # which are loaded with gujarati_consonants.csv.
        # We need to ensure the direct mapping from Gujarati (as 'Arabic' in base class terms) to Devanagari.
        
        # The BaseIndoArabicTransliterator's core conversion path is:
        # text (source) -> isolated_converter -> initial_converter -> hamza_combo -> hamza 
        # -> pass1_converter -> final_converter -> pass2_converter -> final_cleanup -> devanagari_postprocessor

        # For Gujarati -> Devanagari, we are treating Gujarati characters as the "Arabic" input for the base class.
        # The self.arabic_to_devanagari_converter_pass1 and pass2 are built from CONSONANT_MAP_FILES.
        
        text_norm = self.arabic_normalize(text) # Normalize Gujarati text (as if it's an 'Arabic' script variant)

        # If there are Gujarati initial forms or isolated forms like Sindhi, they would be handled here.
        # text_norm = self.isolated_gujarati_to_devanagari_converter.translate(text_norm) # Example
        # text_norm = self.initial_gujarati_to_devanagari_converter.translate(text_norm) # Example
        
        # Hamza processing is specific to Perso-Arabic scripts, might not be relevant for Gujarati.
        # text_norm = self.hamza_combo_to_devanagari_converter.translate(text_norm)
        # text_norm = self.hamza_to_devanagari_converter.translate(text_norm)

        text_trans = self.arabic_to_devanagari_converter_pass1.translate(text_norm)
        # text_trans = self.final_arabic_to_devanagari_converter.translate(text_trans) # Usually for scripts with varying final forms
        text_trans = self.arabic_to_devanagari_converter_pass2.translate(text_trans)
        text_trans = self.arabic_to_devanagari_final_cleanup.translate(text_trans)
        
        text_postprocessed = self.devanagari_postprocessor.translate(text_trans)
        
        if nativize:
            text_postprocessed = self.devanagari_nativize(text_postprocessed)
            
        return text_postprocessed

    def transliterate_from_devanagari_to_gujarati(self, text, nativize=False):
        text_norm = self.devanagari_normalize(text)

        # The reverse transliteration path:
        # devanagari_normalize -> isolated (rev) -> initial (rev) -> hamza (rev) -> hamza_combo (rev)
        # -> pass1 (rev) -> devanagari_remove_short_vowels -> final (rev) -> pass2 (rev) -> final_cleanup (rev)
        # -> source_script_postprocessor (e.g. urdu_postprocessor)

        # text_trans = self.isolated_gujarati_to_devanagari_converter.reverse_translate(text_norm) # Example
        # text_trans = self.initial_gujarati_to_devanagari_converter.reverse_translate(text_norm) # Example
        
        # Hamza not relevant for Devanagari to Gujarati
        # text_trans = self.hamza_to_devanagari_converter.reverse_translate(text_norm)
        # text_trans = self.hamza_combo_to_devanagari_converter.reverse_translate(text_norm)

        text_trans = self.arabic_to_devanagari_converter_pass1.reverse_translate(text_norm)
        # text_trans = self.devanagari_remove_short_vowels(text_trans) # Base class handles this
        # text_trans = self.final_arabic_to_devanagari_converter.reverse_translate(text_trans)
        text_trans = self.arabic_to_devanagari_converter_pass2.reverse_translate(text_trans)
        text_trans = self.arabic_to_devanagari_final_cleanup.reverse_translate(text_trans)
        
        # if nativize:
        #     text_trans = text_trans.translate(gujarati_postprocessor) # Example
            
        return text_trans

    def __call__(self, text, src_lang, dest_lang, nativize=False):
        if src_lang == 'gu' and dest_lang == 'hi': # Assuming 'hi' for Devanagari target
            return self.transliterate_from_gujarati_to_devanagari(text, nativize)
        elif src_lang == 'hi' and dest_lang == 'gu':
            return self.transliterate_from_devanagari_to_gujarati(text, nativize)
        # Add other language pairs if GujaratiTransliterator is to handle them
        # Or raise an error for unsupported pairs
        raise ValueError(f"Unsupported transliteration from {src_lang} to {dest_lang} by GujaratiTransliterator")
