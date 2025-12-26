from flask import Flask, request, jsonify
from flask_cors import CORS
import sys, os
import fitz  # PyMuPDF

# make sure we can import from src
sys.path.insert(0, os.path.dirname(__file__))

from ner_post_processor import NERPostProcessor

app = Flask(__name__)
CORS(app)

processor = NERPostProcessor()

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/process", methods=["POST"])
def process_document():
    """
    Expects a file upload from your existing React UI.
    Returns:
      - entities: processed entities
      - summary.total_entities
      - summary.entity_types
    Your frontend can keep using whatever it already uses for these.
    """
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400

    upload = request.files["file"]
    filename = upload.filename

    # 1) extract text from PDF (simple but works for your demo)
    text = extract_text_from_pdf(upload)

    # 2) build a SIMPLE demo entity dict from that text
    #    (replace this later with your real NER model)
    raw_entities = build_demo_entities(text)

    # 3) run Week‑3 post‑processor
    processed = processor.process(raw_entities, text)
    entities = processed["entities"]

    # 4) compute summary fields your UI needs
    total_entities = sum(len(v) for v in entities.values())
    entity_types = len([k for k, v in entities.items() if v])

    return jsonify(
        {
            "success": True,
            "filename": filename,
            "entities": entities,
            "quality_score": processed["quality_score"],
            "validation_report": processed["validation_report"],
            "summary": {
                "total_entities": total_entities,
                "entity_types": entity_types,
            },
        }
    )

def extract_text_from_pdf(file_storage):
    """Read text from uploaded PDF using PyMuPDF."""
    tmp_path = "temp_upload.pdf"
    file_storage.save(tmp_path)
    text = ""
    try:
        doc = fitz.open(tmp_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception:
        text = ""
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    return text

def build_demo_entities(text: str):
    """
    Very simple heuristic entities so that your UI shows SOMETHING
    even if no ML model is wired yet.
    """
    entities = {"DATE": [], "AMOUNT": [], "ORG": []}

    # crude date detection like 2024-01-15, 15/01/2024, January 15, 2024
    import re
    date_patterns = [
        r"\b\d{4}-\d{1,2}-\d{1,2}\b",
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",
        r"\b\d{1,2}-\d{1,2}-\d{4}\b",
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b",
    ]
    for pat in date_patterns:
        for m in re.finditer(pat, text):
            entities["DATE"].append(
                {"text": m.group(0), "start": m.start(), "end": m.end()}
            )

    # crude amount detection like $125,000 or 125,000.00
    amt_pattern = r"\$[0-9][0-9,]*(?:\.[0-9]{2})?"
    for m in re.finditer(amt_pattern, text):
        entities["AMOUNT"].append(
            {"text": m.group(0), "start": m.start(), "end": m.end()}
        )

    # crude ORG detection: words in ALL CAPS with “LIMITED/INC/LLC/BANK”
    org_pattern = r"\b[A-Z][A-Z &]{2,}\b"
    for m in re.finditer(org_pattern, text):
        entities["ORG"].append(
            {"text": m.group(0).strip(), "start": m.start(), "end": m.end()}
        )

    # remove empty labels
    return {k: v for k, v in entities.items() if v}

if __name__ == "__main__":
    print("Backend running on http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000, debug=True)


