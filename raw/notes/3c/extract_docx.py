import mammoth
import markdownify
import os

files = [
    {
        "in": r"c:\ttluc\Project\learn-ai\tluc-wiki\raw\3c\Checklist 7 ngày thử việc.docx",
        "out": r"c:\ttluc\Project\learn-ai\tluc-wiki\raw\3c\TVV_checklist_7_ngay_v1.md"
    }
]

for item in files:
    if os.path.exists(item["in"]):
        with open(item["in"], "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value
            md = markdownify.markdownify(html, heading_style="ATX")
            
            with open(item["out"], "w", encoding="utf-8") as f:
                f.write(md)
            print(f"Extracted {item['in']} to {item['out']}")
    else:
        print(f"File not found: {item['in']}")
