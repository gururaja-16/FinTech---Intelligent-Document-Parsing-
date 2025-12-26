import re
from typing import Dict

class DateStandardizer:
    """Convert all dates to ISO 8601 format"""
    
    MONTHS = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    @classmethod
    def to_iso8601(cls, date_str: str) -> str:
        """Convert any date format to ISO 8601 (YYYY-MM-DD)"""
        date_str = date_str.strip().strip('.,')
        
        # Pattern 1: January 15, 2024
        m = re.match(r'(\w+)\s+(\d{1,2}),?\s+(\d{4})', date_str)
        if m:
            month = cls.MONTHS.get(m.group(1).lower())
            if month:
                return f"{m.group(3)}-{month:02d}-{int(m.group(2)):02d}"
        
        # Pattern 2: 15-01-2024 or 15/01/2024
        m = re.match(r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})', date_str)
        if m:
            day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if 1 <= month <= 12:
                return f"{year}-{month:02d}-{day:02d}"
        
        # Pattern 3: 2024-01-15
        m = re.match(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', date_str)
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        
        return date_str
    
    @classmethod
    def standardize_entities(cls, entities: Dict) -> Dict:
        """Standardize all DATE entities in extracted entities"""
        standardized = {}
        for label, items in entities.items():
            if label == 'DATE':
                standardized[label] = [
                    {
                        'original': item['text'],
                        'standardized': cls.to_iso8601(item['text']),
                        'start': item.get('start'),
                        'end': item.get('end')
                    }
                    for item in items
                ]
            else:
                standardized[label] = items
        return standardized
