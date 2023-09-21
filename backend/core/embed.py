from utils.logger import log

from typing import List
from utils.configs import embedding_configs

from sentence_transformers import SentenceTransformer

model: SentenceTransformer

def init():
    log.info(f"Initialising embedding model {embedding_configs.model}")
    global model
    model = SentenceTransformer(embedding_configs.model)
    log.info('Embedding model initialised')

def embed_text(text) -> List[float]:
    return model.encode([text])[0].tolist()
