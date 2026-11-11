from functools import lru_cache

from sentence_transformers import SentenceTransformer


# lru_cache makes this load the model once and reuse it. Loading takes seconds,
# and the first ever call downloads ~90 MB from Hugging Face.
@lru_cache
def _model() -> SentenceTransformer:
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> list[list[float]]:
    # normalize_embeddings makes cosine distance behave properly.
    vectors = _model().encode(texts, normalize_embeddings=True, batch_size=32)
    return vectors.tolist()
