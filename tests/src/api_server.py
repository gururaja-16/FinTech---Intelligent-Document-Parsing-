# Add this import at top
from ner_post_processor import NERPostProcessor

# Replace your NER processing with this:
processor = NERPostProcessor()
processed_result = processor.process(entities, text)
entities = processed_result['entities']
quality_score = processed_result['quality_score']
warnings = processed_result['validation_report']

# Return enhanced response
return jsonify({
    'success': True,
    'text': text,
    'entities': entities,           # ← Now CLEAN + STANDARDIZED
    'quality_score': quality_score, # ← NEW: 0-1 confidence
    'warnings': warnings,           # ← NEW: validation issues
    'summary': {
        'total_entities': sum(len(v) for v in entities.values()),
        'quality': f"{quality_score:.2f}"
    }
})
