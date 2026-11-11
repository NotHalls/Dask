# TODO: this method is good for starters but it might cut a word right in the middle
# So, we need somethign that can snap to the nearest space or something

def chunk_text(text: str, size: int = 1000, overlap: int = 200) -> list[str]:
  if overlap >= size:
    raise ValueError("Chunking Overlap Size Can't Be The Same As Chunk Size Itself!")

  chunks = []
  start = 0

  while start < len(text):
    end = start + size
    piece = text[start:end].strip()

    if piece:
      chunks.append(piece)
    if end >= len(text):
      break

    start = end - overlap

  return chunks
