import spacy
from spacy.training import Example
import json

print("🎯 WEEK 2: NER MODEL TRAINING")

nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

labels = ["PARTY", "DATE", "AMOUNT", "JURISDICTION"]
for label in labels:
    ner.add_label(label)

# Load annotation
with open("data/annotated/contract_01.json") as f:
    data = json.load(f)

text = data["text"]
train_data = []
for label, entities in data["entities"].items():
    for entity in entities:
        start = text.find(entity)
        if start != -1:
            end = start + len(entity)
            doc = nlp.make_doc(text)
            ex = Example.from_dict(doc, {"entities": [(start, end, label)]})
            train_data.append(ex)

print(f"📊 {len(train_data)} training examples")

# Train
optimizer = nlp.begin_training()
for i in range(20):
    losses = {}
    nlp.update(train_data, drop=0.3, sgd=optimizer, losses=losses)
    if i % 5 == 0:
        print(f"Epoch {i+1}/20 | Loss: {losses}")

nlp.to_disk("models/legal_ner")
print("\n✅ WEEK 2 NER MODEL READY!")

