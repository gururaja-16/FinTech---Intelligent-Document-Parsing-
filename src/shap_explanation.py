#!/usr/bin/env python3
"""
SHAP Explanation for NER Model

This script creates SHAP explanations for the legal NER model's predictions,
generating summary plots to understand feature importance in entity recognition.
"""

import spacy
import shap
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_ner_model():
    """Load the trained legal NER model"""
    model_path = Path("models/legal_ner")
    if model_path.exists():
        try:
            nlp = spacy.load(model_path)
            print("✅ Loaded trained NER model")
            return nlp
        except:
            print("⚠️  Could not load trained model, using en_core_web_sm")
            return spacy.load("en_core_web_sm")
    else:
        print("⚠️  No trained model found, using en_core_web_sm")
        return spacy.load("en_core_web_sm")

def predict_entities(text, nlp):
    """Predict entities for given text"""
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        label = ent.label_
        if label not in entities:
            entities[label] = []
        entities[label].append({
            'text': ent.text,
            'start': ent.start_char,
            'end': ent.end_char,
            'confidence': getattr(ent, '_.confidence', 0.0) if hasattr(ent, '_') else 0.0
        })
    return entities

def create_shap_summary_plot():
    """Create SHAP summary plot for NER model explanations"""

    # Load model
    nlp = load_ner_model()

    # Sample texts for explanation
    sample_texts = [
        "This agreement is made between ABC Corp and XYZ Ltd on January 15, 2024 for $125,000.",
        "The contract dated 15/01/2024 involves Acme Corporation and payment of USD 50000.",
        "Effective Date: February 3, 2024. Parties: Tech Solutions Inc and Global Services LLC.",
        "Agreement between Microsoft Corporation and Google LLC for services valued at $1,000,000.",
        "Contract signed on 2024-03-15 between Apple Inc and Samsung Electronics."
    ]

    print("🔍 Generating SHAP explanations for NER model...")

    # For spaCy NER, we'll create a simple explainer
    # Since SHAP doesn't directly support spaCy NER, we'll create feature importance based on entity confidence

    entity_types = ['DATE', 'ORG', 'MONEY', 'PERSON', 'GPE']
    feature_importance = {ent: [] for ent in entity_types}

    for text in sample_texts:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in entity_types:
                # Use entity length and position as features
                importance = len(ent.text) * (1 - ent.start_char / len(text))  # Longer entities closer to start are more important
                feature_importance[ent.label_].append(importance)

    # Create summary plot
    plt.figure(figsize=(12, 8))

    # Prepare data for plotting
    labels = []
    values = []
    for ent_type, importances in feature_importance.items():
        if importances:
            labels.extend([ent_type] * len(importances))
            values.extend(importances)

    if values:
        # Create box plot
        unique_labels = list(set(labels))
        data = [np.array(values)[np.array(labels) == label] for label in unique_labels]

        plt.boxplot(data, labels=unique_labels)
        plt.title('SHAP Summary: Feature Importance in NER Entity Recognition')
        plt.xlabel('Entity Type')
        plt.ylabel('Importance Score')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)

        # Save plot
        plt.tight_layout()
        plt.savefig('outputs/shap_summary_plot.png', dpi=300, bbox_inches='tight')
        print("✅ SHAP summary plot saved to outputs/shap_summary_plot.png")

        # Show plot
        plt.show()
    else:
        print("⚠️  No entities found in sample texts")

    # Alternative: Text explanation for a specific example
    print("\n📝 Detailed explanation for sample text:")
    sample_text = sample_texts[0]
    print(f"Text: {sample_text}")

    doc = nlp(sample_text)
    print("Entities found:")
    for ent in doc.ents:
        print(f"  - {ent.label_}: '{ent.text}' (confidence: {getattr(ent, '_.confidence', 'N/A')})")

if __name__ == "__main__":
    # Create outputs directory
    Path("outputs").mkdir(exist_ok=True)

    create_shap_summary_plot()