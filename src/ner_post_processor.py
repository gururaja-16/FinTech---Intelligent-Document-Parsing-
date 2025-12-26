from typing import Dict, List
from validation_rules import ValidationRules
from date_standardizer import DateStandardizer

class NERPostProcessor:
    """Complete post-processing pipeline for NER output"""
    
    def __init__(self):
        self.validator = ValidationRules()
        self.date_std = DateStandardizer()
    
    def process(self, entities: Dict, text: str) -> Dict:
        """Main pipeline: Clean → Standardize → Validate → Score"""
        
        # 1. Clean text
        cleaned = self._clean_entities(entities)
        
        # 2. Standardize dates
        standardized = self.date_std.standardize_entities(cleaned)
        
        # 3. Standardize amounts
        standardized = self._standardize_amounts(standardized)
        
        # 4. Add heuristic entities
        heuristics = self._extract_heuristics(text)
        final = self._merge_entities(standardized, heuristics)
        
        # 5. Validate constraints
        report = self._validate_constraints(final)
        
        return {
            'entities': final,
            'validation_report': report,
            'quality_score': self._calculate_quality(final, report)
        }
    
    def _clean_entities(self, entities: Dict) -> Dict:
        cleaned = {}
        for label, items in entities.items():
            cleaned[label] = [
                {
                    **item,
                    'text': self.validator.clean_entity_text(item['text'])
                }
                for item in items
            ]
        return cleaned
    
    def _standardize_amounts(self, entities: Dict) -> Dict:
        if 'AMOUNT' not in entities:
            return entities
        
        result = {}
        for label, items in entities.items():
            if label == 'AMOUNT':
                result[label] = [
                    {
                        'original': item['text'],
                        **self.validator.standardize_amount(item['text']),
                        'start': item.get('start'),
                        'end': item.get('end')
                    }
                    for item in items
                ]
            else:
                result[label] = items
        return result
    
    def _extract_heuristics(self, text: str) -> Dict:
        parties = self.validator.extract_party_names(text)
        heuristics = {}
        if parties:
            heuristics['PARTY_HEURISTIC'] = [
                {'text': party, 'source': 'heuristic'}
                for party in parties
            ]
        return heuristics
    
    def _merge_entities(self, ml_entities: Dict, heuristics: Dict) -> Dict:
        merged = ml_entities.copy()
        for label, items in heuristics.items():
            if label not in merged:
                merged[label] = []
            merged[label].extend(items)
        return merged
    
    def _validate_constraints(self, entities: Dict) -> List[str]:
        warnings = []
        
        # Date logic check
        dates = entities.get('DATE', [])
        eff_dates = [d.get('standardized', d.get('text', '')) for d in dates if 'effective' in str(d).lower()]
        term_dates = [d.get('standardized', d.get('text', '')) for d in dates if 'terminat' in str(d).lower()]
        
        if eff_dates and term_dates:
            valid, msg = self.validator.validate_date_logic(eff_dates[0], term_dates[0])
            warnings.append(f"Date Logic: {msg}")
        
        if not entities.get('AMOUNT'):
            warnings.append("WARNING: No amount found")
        if not any('PARTY' in k for k in entities.keys()):
            warnings.append("WARNING: No parties found")
            
        return warnings
    
    def _calculate_quality(self, entities: Dict, report: List) -> float:
        score = 0.0
        
        # Entity coverage
        types_found = len([k for k, v in entities.items() if v])
        score += min(types_found * 0.25, 1.0)
        
        # Penalty for warnings
        score -= len(report) * 0.1
        
        return max(0.0, min(1.0, score))
