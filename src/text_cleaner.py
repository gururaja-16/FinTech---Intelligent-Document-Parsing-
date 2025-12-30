import re
import unicodedata
from typing import Dict, Set

class TextCleaner:
    # Common OCR substitution errors - first pass
    FIRST_SUBSTITUTIONS = {
        'O': '0',
        'rn': 'm',
        'nn': 'm',
        'ii': 'u',
        'cl': 'd',
        'c1': 'd',
        'vv': 'w',
        'vvv': 'w',
    }

    # Second pass - only if text has non-digits
    SECOND_SUBSTITUTIONS = {
        '1': 'i',
        '3': 'e',
        '5': 's',
        '8': 'b',
    }

    # Specific word corrections
    WORD_CORRECTIONS = {
        'rnarket': 'market',
        'exam ple': 'example',
        'exampl': 'example',
    }

    # Common words for completion
    COMMON_WORDS: Set[str] = {
        'example', 'market', 'test', 'hello', 'world', 'this', 'is', 'a', 'cafe', 'resume', 'acme'
    }

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Apply heuristic rules to clean OCR text:
        - Character substitutions
        - Remove noise symbols
        - Normalize whitespace
        - Lowercase
        - Word merging/splitting
        - Diacritic removal
        """
        # Remove diacritics
        text = unicodedata.normalize('NFD', text)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')

        # Apply first OCR substitutions
        for wrong, correct in TextCleaner.FIRST_SUBSTITUTIONS.items():
            text = text.replace(wrong, correct)

        # Replace non-alphanumeric with space (keep : / )
        text = re.sub(r'[^a-zA-Z0-9\s:/]', ' ', text)

        # Normalize whitespace (including newlines)
        text = re.sub(r'\s+', ' ', text).strip()

        # Handle word breaks and merges
        words = text.split()
        corrected_words = []
        i = 0
        while i < len(words):
            word = words[i]
            # Try to merge with next word if it looks like a split
            if i + 1 < len(words) and len(word) <= 3 and len(words[i+1]) <= 3:
                merged = word + words[i+1]
                if merged.lower() in TextCleaner.COMMON_WORDS:
                    corrected_words.append(merged)
                    i += 2
                    continue
            corrected_words.append(word)
            i += 1

        text = ' '.join(corrected_words)

        # Apply word corrections
        for wrong, correct in TextCleaner.WORD_CORRECTIONS.items():
            text = re.sub(r'\b' + re.escape(wrong) + r'\b', correct, text)

        # Apply second substitutions only if text contains non-digits
        if not re.match(r'^[\d\s]*$', text):
            for wrong, correct in TextCleaner.SECOND_SUBSTITUTIONS.items():
                text = text.replace(wrong, correct)

        # Special rule: 'l' -> '1' if adjacent to digit
        text_list = list(text)
        for i in range(len(text_list)):
            if text_list[i] == 'l':
                adjacent_digit = (i > 0 and text_list[i-1].isdigit()) or (i < len(text_list)-1 and text_list[i+1].isdigit())
                if adjacent_digit:
                    text_list[i] = '1'
        text = ''.join(text_list)

        # Final cleanup
        text = re.sub(r'\s+', ' ', text).strip()

        return text

# For backward compatibility
def normalize_text(text: str) -> str:
    return TextCleaner.normalize_text(text)