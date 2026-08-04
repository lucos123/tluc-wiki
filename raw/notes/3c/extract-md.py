import pymupdf4llm
import os

base_dir = r"c:\ttluc\Project\learn-ai\tluc-wiki\raw\3c"
files = [
    "quytrinhtuvan_v1.pdf",
    "TVV_implant_ghepxuong_v1.pdf",
    "TVV_rangsu_veneer_v1.pdf",
    "TVV_thamkhao_v1.pdf"
]

for filename in files:
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        print(f"Processing {filename}...")
        try:
            md_text = pymupdf4llm.to_markdown(filepath)
            outpath = filepath.replace('.pdf', '.md')
            with open(outpath, 'w', encoding='utf-8') as f:
                f.write(md_text)
            print(f"Successfully wrote {outpath}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    else:
        print(f"File not found: {filepath}")
