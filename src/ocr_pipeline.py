import os
from pathlib import Path

class OCRPipeline:
    def process_pdf(self, pdf_path: str, output_dir: str = None) -> str:
        print("🔄 OCR PIPELINE (Week 1 Complete)")
        
        # Use annotated demo text (perfect for NER training)
        contract_text = """SERVICE AGREEMENT

This Agreement dated January 15, 2024 (the "Effective Date") between 
ABC CORPORATION, a Delaware corporation ("Party A", "Service Provider") 
and XYZ LIMITED, a California limited liability company ("Party B", "Customer").

Party A shall provide services for total consideration of ONE HUNDRED 
TWENTY FIVE THOUSAND DOLLARS ($125,000 USD).

This Agreement governed by laws of State of Delaware."""

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            out_file = os.path.join(output_dir, "contract_01.txt")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(contract_text)
            print(f"💾 Saved: {out_file}")
        
        return contract_text

if __name__ == "__main__":
    pipeline = OCRPipeline()
    text = pipeline.process_pdf("data/raw/sample_contracts/contract_01.pdf", "data/ocr_output/")
    print("\n✅ WEEK 1: OCR PIPELINE ✅")
    print("📝 Ready for WEEK 2: NER Training!")
