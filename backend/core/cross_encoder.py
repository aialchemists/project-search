from utils.logger import log

from sentence_transformers import CrossEncoder

_MODEL_NAME = 'cross-encoder/ms-marco-MiniLM-L-2-v2'

ce_model: CrossEncoder

def init():
    log.info(f"Loading CrossEncoder model {_MODEL_NAME}")
    global ce_model
    ce_model = CrossEncoder(_MODEL_NAME)
    log.info('CrossEncoder model loaded')

def rank(user_query, chunks, chunk_ids, top_k):
    sentence_pairs = [[user_query, chunk] for chunk in chunks]

    # Calculate similarity using Cross encoder
    scores = ce_model.predict(sentence_pairs)

    # Combine the scores with sentence pairs
    combined_scores = list(zip(sentence_pairs, scores, chunk_ids))

    # Sort the pairs by Cross Encoder scores
    sorted_pairs = sorted(combined_scores, key=lambda x: x[1], reverse=True)

    # Return the top N pairs and their similarity scores
    top_pairs = sorted_pairs[:top_k]

    return top_pairs
