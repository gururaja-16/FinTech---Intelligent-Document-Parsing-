import unittest
import sys
sys.path.insert(0, '../src')

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
