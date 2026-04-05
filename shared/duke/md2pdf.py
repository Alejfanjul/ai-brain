import markdown
import subprocess
import os
import sys
import time

md_file = sys.argv[1]
pdf_file = sys.argv[2]

with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    margin: 25mm 20mm;
    size: A4;
  }}
  body {{
    font-family: 'Segoe UI', Calibri, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
    padding: 20px 40px;
  }}
  h1 {{
    font-size: 20pt;
    border-bottom: 2px solid #2c3e50;
    padding-bottom: 8px;
    margin-top: 0;
  }}
  h2 {{
    font-size: 14pt;
    color: #2c3e50;
    margin-top: 24px;
    border-bottom: 1px solid #bdc3c7;
    padding-bottom: 4px;
  }}
  h3 {{
    font-size: 12pt;
    color: #34495e;
    margin-top: 16px;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 10pt;
  }}
  th, td {{
    border: 1px solid #bdc3c7;
    padding: 8px 10px;
    text-align: left;
  }}
  th {{
    background-color: #2c3e50;
    color: white;
    font-weight: 600;
  }}
  tr:nth-child(even) {{
    background-color: #f8f9fa;
  }}
  strong {{
    color: #2c3e50;
  }}
  blockquote {{
    border-left: 3px solid #2c3e50;
    margin: 12px 0;
    padding: 8px 16px;
    background: #f8f9fa;
    font-style: italic;
  }}
  hr {{
    border: none;
    border-top: 1px solid #ddd;
    margin: 24px 0;
  }}
  ul {{
    padding-left: 20px;
  }}
  li {{
    margin-bottom: 4px;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

# Write HTML next to the markdown file (persistent, not temp)
html_path = os.path.abspath(os.path.join(os.path.dirname(md_file), "_proposta.html"))
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"HTML gerado: {html_path}")

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
pdf_abs = os.path.abspath(pdf_file)

# Use Windows-native path for Edge
result = subprocess.run([
    edge,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    f"--print-to-pdf={pdf_abs}",
    "--no-pdf-header-footer",
    html_path
], capture_output=True, timeout=30, text=True)

print(f"stdout: {result.stdout}")
print(f"stderr: {result.stderr}")
print(f"returncode: {result.returncode}")

if os.path.exists(pdf_abs):
    size = os.path.getsize(pdf_abs)
    print(f"PDF gerado: {pdf_abs} ({size} bytes)")
else:
    print("PDF NAO foi gerado")
