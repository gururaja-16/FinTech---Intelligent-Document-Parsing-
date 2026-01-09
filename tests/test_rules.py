import unittest
import sys
sys.path.insert(0, '../src')

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dateutil import parser


from validation_rules import ValidationRules
from date_standardizer import DateStandardizer
from ner_post_processor import NERPostProcessor

class TestDateStandardization(unittest.TestCase):
    def test_full_month_name(self):
        result = DateStandardizer.to_iso8601("January 15, 2024")
        self.assertEqual(result, "2024-01-15")
    
    def test_abbreviated_month(self):
        result = DateStandardizer.to_iso8601("Jan 15, 2024")
        self.assertEqual(result, "2024-01-15")
    
    def test_dmy_format(self):
        result = DateStandardizer.to_iso8601("15-01-2024")
        self.assertEqual(result, "2024-01-15")
    
    def test_ymd_format(self):
        result = DateStandardizer.to_iso8601("2024-01-15")
        self.assertEqual(result, "2024-01-15")
    
    def test_with_punctuation(self):
        result = DateStandardizer.to_iso8601("January 15, 2024.")
        self.assertEqual(result, "2024-01-15")

class TestAmountStandardization(unittest.TestCase):
    def test_dollar_with_commas(self):
        result = ValidationRules.standardize_amount("$125,000")
        self.assertEqual(result['value'], 125000.0)
        self.assertEqual(result['currency'], '$')
    
    def test_decimal_amount(self):
        result = ValidationRules.standardize_amount("$1,234.56")
        self.assertEqual(result['value'], 1234.56)
    
    def test_usd_prefix(self):
        result = ValidationRules.standardize_amount("USD 50000")
        self.assertEqual(result['value'], 50000.0)

class TestDateLogicValidation(unittest.TestCase):
    def test_valid_sequence(self):
        valid, msg = ValidationRules.validate_date_logic("2024-01-15", "2024-12-31")
        self.assertTrue(valid)
    
    def test_invalid_sequence(self):
        valid, msg = ValidationRules.validate_date_logic("2024-12-31", "2024-01-15")
        self.assertFalse(valid)
    
    def test_same_dates(self):
        valid, msg = ValidationRules.validate_date_logic("2024-01-15", "2024-01-15")
        self.assertFalse(valid)

class TestEntityCleaning(unittest.TestCase):
    def test_remove_extra_spaces(self):
        result = ValidationRules.clean_entity_text("ABC   CORP  ")
        self.assertEqual(result, "ABC CORP")
    
    def test_remove_quotes(self):
        result = ValidationRules.clean_entity_text('"ABC CORP"')
        self.assertEqual(result, "ABC CORP")

class TestPartyExtraction(unittest.TestCase):
    def test_extract_parties(self):
        text = "Agreement between ABC Corp and XYZ Ltd for services."
        parties = ValidationRules.extract_party_names(text)
        self.assertTrue(len(parties) >= 1)
        self.assertTrue(any('ABC' in p for p in parties))

class TestNERPostProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = NERPostProcessor()
    
    def test_full_pipeline(self):
        entities = {
            'DATE': [{'text': 'January 15, 2024', 'start': 0, 'end': 17}],
            'AMOUNT': [{'text': '$125,000', 'start': 50, 'end': 58}]
        }
        text = "Agreement dated January 15, 2024 for $125,000"
        result = self.processor.process(entities, text)
        
        self.assertIn('entities', result)
        self.assertIn('quality_score', result)
        self.assertGreater(result['quality_score'], 0)
    
    def test_quality_score_range(self):
        entities = {'DATE': []}
        text = "test"
        result = self.processor.process(entities, text)
        self.assertGreaterEqual(result['quality_score'], 0.0)
        self.assertLessEqual(result['quality_score'], 1.0)

if __name__ == '__main__':
    unittest.main()
    
    
import pytest
from text_cleaner import normalize_text

@pytest.mark.parametrize("input_text,expected", [
    ("Th1s is a t3st", "This is a test"),
    ("exam ple", "Example"),
    ("rnarket", "Market"),
    ("@hello#world$", "hello world"),
    ("tEsT", "tEsT"),
    ("exampl", "Example"),
    ("café résumé", "cafe resume"),
    ("This\nis\na\ntest", "This is a test"),
    ("O123", "0123"),
])
def test_normalize_text(input_text, expected):
    assert normalize_text(input_text) == expected


class TestAdvancedEdgeCases(unittest.TestCase):
    def test_effective_date_ocr_confusion(self):
        result = normalize_text("Effect1ve Date: 0l/02/2024")
        self.assertEqual(result, "Effective Date: 01/02/2024")
    
    def test_party_name_with_symbols(self):
        result = normalize_text("@Acme#Corp$ Pvt. Ltd.")
        self.assertEqual(result, "Acme Corp Pvt Ltd")
    
    def test_jurisdiction_diacritics(self):
        result = normalize_text("Jurisdiction: São Paulo, Brazil")
        self.assertEqual(result, "Jurisdiction: Sao Paulo, Brazil")
    
    def test_effective_date_line_breaks(self):
        result = normalize_text("Effective\nDate:\nFebruary 3, 2024")
        self.assertEqual(result, "Effective Date: February 3, 2024")
    
    def test_party_name_split(self):
        result = normalize_text("Ac me Corporation")
        self.assertEqual(result, "Acme Corporation")
    
    def test_noise_only(self):
        result = normalize_text("@@@###$$$")
        self.assertEqual(result, "")
    
    def test_amount_ocr_confusion(self):
        result = normalize_text("Total Value: USD 10O,OOO")
        self.assertEqual(result, "Total Value: USD 100,000")
    
    def test_date_logic_validation_invalid(self):
        valid, msg = ValidationRules.validate_date_logic("01/01/2024", "12/31/2023")
        self.assertFalse(valid)
        self.assertIn("precedes", msg)
    
    def test_currency_indian_grouping(self):
        result = ValidationRules.standardize_amount("INR 1,00,000.00")
        self.assertEqual(result['value'], 100000.0)
        self.assertEqual(result['currency'], 'INR')
    
    def test_mixed_date_formats(self):
        from date_standardizer import DateStandardizer
        date1 = DateStandardizer.to_iso8601("03/02/2024")
        date2 = DateStandardizer.to_iso8601("March 5, 2024")
        self.assertEqual(date1, "2024-02-03")
        self.assertEqual(date2, "2024-03-05")

