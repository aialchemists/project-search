# Need to integrate with remaining code, add model to config

from sentence_transformers import CrossEncoder

def rerank_query_chunk_pair(user_query, chunks, top_k):
    ce_model = CrossEncoder('cross-encoder/stsb-roberta-large')

    sentence_pairs = [[user_query, chunk] for chunk in chunks]

    # Calculate similarity using Cross encoder
    scores = ce_model.predict(sentence_pairs)

    # Combine the scores with sentence pairs
    combined_scores = list(zip(sentence_pairs, scores))

    # Sort the pairs by Cross Encoder scores
    sorted_pairs = sorted(combined_scores, key=lambda x: x[1], reverse=True)

    # Return the top N pairs and their similarity scores
    top_pairs = sorted_pairs[:top_k]

    return top_pairs
