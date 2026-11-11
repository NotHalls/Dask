from pypdf import PdfReader

def extract_pages(file) -> list[tuple[int, str]]:
  reader = PdfReader(file)
  pages = []

  for index, page in enumerate(reader.pages):
    text = page.extract_text() or ""
    if text.strip():
      pages.append((index + 1, text))

  return pages
