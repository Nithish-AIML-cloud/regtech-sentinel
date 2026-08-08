import pdfplumber
import os
import json

raw_folder = "data/raw"
processed_folder = "data/processed"

# Get list of all PDF files in raw folder
pdf_files = [f for f in os.listdir(raw_folder) if f.endswith(".pdf")]
print("Found PDFs:", pdf_files)

for filename in pdf_files:
    pdf_path = os.path.join(raw_folder, filename)
    
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"
        
        total_pages = len(pdf.pages)
    
    # Build a dictionary to store metadata + text
    document_data = {
        "filename": filename,
        "total_pages": total_pages,
        "text": all_text
    }
    
    # Save as JSON with the same name (but .json extension)
    output_filename = filename.replace(".pdf", ".json")
    output_path = os.path.join(processed_folder, output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(document_data, f, ensure_ascii=False, indent=2)
    
    print(f"Processed {filename}: {total_pages} pages, saved to {output_filename}")

print("Done!")

