import os
from TextExtractor import TextExtractor

# Define directory paths
ROOT_DIR = "./"
RAW_DIR = os.path.join(ROOT_DIR, "data/raw/akumin")
PROCESSED_ROOT = os.path.join(ROOT_DIR, "data/processed/akumin")
MODES = ["pdfplumber", "pymupdf", "tesseract", "pymupdf4llm"]
# MODES = ["pymupdf4llm"]

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    ensure_dir(RAW_DIR)
    ensure_dir(PROCESSED_ROOT)

    pdf_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".pdf")]
    print(f"📄 Found PDF files: {pdf_files}")
    
    extractor = TextExtractor()

    for file in pdf_files:
        input_file_path = os.path.join(RAW_DIR, file)
        contract_name = os.path.splitext(file)[0]
        output_dir = os.path.join(PROCESSED_ROOT, contract_name)
        ensure_dir(output_dir)

        for mode in MODES:
            print(f"🔍 Processing {file} in mode '{mode}'")

            try:
                # if mode == 'pymupdf4llm' and not hasattr(extractor, 'extract_with_pymupdf4llm'):
                #     print("⚠️ Skipping pymupdf4llm (not available)")
                #     continue

                result_text = extractor.extract_text(input_file_path, output_dir, mode=mode)

                if mode == 'pymupdf4llm':
                    # Save as .md
                    output_md_file = os.path.join(output_dir, f"{contract_name}_{mode}.md")
                    with open(output_md_file, "w", encoding="utf-8") as f:
                        f.write(result_text)
                    print(f"✅ Saved Markdown: {output_md_file}")

                    # Save as .txt (same content as .md, but with .txt extension)
                    output_txt_file = os.path.join(output_dir, f"{contract_name}_{mode}.txt")
                    with open(output_txt_file, "w", encoding="utf-8") as f:
                        f.write(result_text)
                    print(f"✅ Saved Plain Text (Markdown content): {output_txt_file}")
                else:
                    # Original saving logic for other modes (if MODES was expanded)
                    output_file = os.path.join(output_dir, f"{contract_name}_{mode}.txt")
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(result_text) # result_text is already a string
                    print(f"✅ Saved: {output_file}")
                
                
                # output_file = os.path.join(output_dir, f"{contract_name}_{mode}.txt")
                # with open(output_file, "w", encoding="utf-8") as f:
                #     if isinstance(result, dict) and "text" in result:
                #         f.write(result["text"])
                #     elif isinstance(result, dict) and "pages" in result:
                #         f.write("\n".join(result["pages"]))
                #     elif isinstance(result, str):
                #         f.write(result)
                #     else:
                #         f.write(str(result))
                # 
                # print(f"✅ Saved: {output_file}")

            except Exception as e:
                print(f"Failed to process {file} in mode {mode}: {e}")

if __name__ == "__main__":
    main()
