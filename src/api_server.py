from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pathlib import Path
import spacy
from ocr_pipeline import OCRPipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Get the absolute path to the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "legal_ner")

# Initialize OCR Pipeline
ocr_pipeline = OCRPipeline()

# Load trained NER model
try:
    nlp = spacy.load(MODEL_PATH)
    print("✅ NER Model loaded successfully")
except Exception as e:
    print(f"⚠️ NER Model not found at {MODEL_PATH}")
    print(f"Error: {e}")
    nlp = None

# Create upload directory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': nlp is not None
    })

@app.route('/api/process-document', methods=['POST'])
def process_document():
    """Process uploaded document and extract entities"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Process with OCR (or use demo text)
        text = ocr_pipeline.process_pdf(file_path)
        
        # Extract entities using NER
        entities = {}
        if nlp:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append({
                    'text': ent.text,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return jsonify({
            'success': True,
            'text': text,
            'entities': entities,
            'summary': {
                'total_entities': sum(len(v) for v in entities.values()),
                'entity_types': len(entities)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """Analyze text directly without file upload"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Extract entities using NER
        entities = {}
        if nlp:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append({
                    'text': ent.text,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
        
        return jsonify({
            'success': True,
            'entities': entities,
            'summary': {
                'total_entities': sum(len(v) for v in entities.values()),
                'entity_types': len(entities)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting FinTech Document Parser API Server...")
    print("📡 Server running on http://localhost:5000")
    print("📝 Endpoints:")
    print("   - GET  /api/health")
    print("   - POST /api/process-document")
    print("   - POST /api/analyze-text")
    app.run(debug=True, port=5000, host='0.0.0.0')
