from typing import List
from utils.configs import embedding_configs

from sentence_transformers import SentenceTransformer
model = SentenceTransformer(embedding_configs.model)

def embed_text(text) -> List[float]:
    return model.encode([text])[0].tolist()
