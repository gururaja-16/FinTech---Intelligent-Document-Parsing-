import re
from datetime import datetime
from typing import Dict, List, Tuple

class ValidationRules:
    @staticmethod
    def standardize_date(date_text: str) -> str:
        date_patterns = [
            (r'(\w+)\s+(\d{1,2}),\s+(\d{4})', lambda m: ValidationRules._parse_mdy(m)),
            (r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})', lambda m: ValidationRules._parse_dmy(m)),
            (r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', lambda m: ValidationRules._parse_ymd(m)),
            (r'([A-Za-z]{3})\s+(\d{1,2}),?\s+(\d{4})', lambda m: ValidationRules._parse_abbr_mdy(m)),
        ]
        
        for pattern, parser in date_patterns:
            match = re.search(pattern, date_text)
            if match:
                try:
                    return parser(match)
                except:
                    pass
        return date_text
    
    @staticmethod
    def _parse_mdy(match):
        months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
                  'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
        month = months.get(match.group(1).lower(), 1)
        day = int(match.group(2))
        year = int(match.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"
    
    @staticmethod
    def _parse_dmy(match):
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"
    
    @staticmethod
    def _parse_ymd(match):
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"
    
    @staticmethod
    def _parse_abbr_mdy(match):
        months = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                  'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
        month = months.get(match.group(1).lower(), 1)
        day = int(match.group(2))
        year = int(match.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"
    
    @staticmethod
    def standardize_amount(amount_text: str) -> Dict:
        pattern = r'(\$|USD|EUR|GBP)?\s*([0-9,]+\.?[0-9]*)'
        match = re.search(pattern, amount_text)
        if match:
            currency = match.group(1) or 'USD'
            value = match.group(2).replace(',', '')
            return {
                'original': amount_text,
                'value': float(value),
                'currency': currency,
                'formatted': f"{currency} {float(value):,.2f}"
            }
        return {'original': amount_text, 'value': None, 'currency': None}
    
    @staticmethod
    def validate_date_logic(effective_date: str, termination_date: str) -> Tuple[bool, str]:
        try:
            eff = datetime.strptime(effective_date, '%Y-%m-%d')
            term = datetime.strptime(termination_date, '%Y-%m-%d')
            if term > eff:
                return True, "Valid: Termination date is after effective date"
            else:
                return False, f"ERROR: Termination date ({termination_date}) must be after Effective date ({effective_date})"
        except:
            return False, "Date parsing error"
    
    @staticmethod
    def clean_entity_text(entity_text: str) -> str:
        text = re.sub(r'\s+', ' ', entity_text).strip()
        text = text.strip("\"'")
        return text
    
    @staticmethod
    def extract_party_names(text: str) -> List[str]:
        pattern = r'between\s+([A-Z][A-Za-z\s&.,]+?)\s+and\s+([A-Z][A-Za-z\s&.,]+?)(?:\s+for|\s+on|\s+,|\.)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        parties = []
        for match in matches:
            for party in match:
                if party:
                    parties.append(ValidationRules.clean_entity_text(party))
        return list(set(parties))



