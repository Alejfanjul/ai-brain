---
name: CapturePdf
description: Capture PDF books to ai-brain sources. USE WHEN user wants to capture pdf, import pdf, add pdf book, process pdf for embeddings OR /capture-pdf OR /pdf.
---

# CapturePdf

Captures PDF books and converts them to markdown for the ai-brain knowledge base.

## How It Works

1. Extracts text from all PDF pages
2. Cleans content (removes tracking, formatting artifacts)
3. Saves as markdown in `sources/`
4. Auto-commits to git
5. Ready for embedding via `embed_sources.py`

## Usage

**Basic (interactive - will prompt for author/title if not in PDF metadata):**
```bash
python3 ~/ai-brain/scripts/capture_pdf.py /path/to/book.pdf
```

**With metadata (recommended for cleaner filenames):**
```bash
python3 ~/ai-brain/scripts/capture_pdf.py /path/to/book.pdf --author "Author Name" --title "Book Title"
```

**Without auto-commit:**
```bash
python3 ~/ai-brain/scripts/capture_pdf.py /path/to/book.pdf --no-commit
```

## After Capture

Generate embeddings for the new content:
```bash
python3 ~/ai-brain/scripts/embed_sources.py
```

## Examples

**Example 1: Capture a fitness book**
```
User: "/capture-pdf"
User provides: /home/user/downloads/531-forever.pdf
→ Runs capture script with --author "Jim Wendler" --title "5/3/1 Forever"
→ Creates sources/2026-01-18-jim-wendler-531-forever.md
→ Commits to git
→ User runs embed_sources.py to index
```

**Example 2: Capture with prompts**
```
User: "capture this pdf ~/books/some-book.pdf"
→ Runs capture script
→ Script prompts for author/title if not detected
→ Creates markdown in sources/
→ Ready for embeddings
```

**Example 3: Batch capture**
```
User: "I have 3 Wendler PDFs to capture"
→ Run capture script for each PDF
→ Then run embed_sources.py once at the end
```
