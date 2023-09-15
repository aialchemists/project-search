# Need to integrate with remaining code, add model to config

from sentence_transformers import CrossEncoder

def rerank_query_chunk_pair(sentence_pairs, top_n):
    ce_model = CrossEncoder('cross-encoder/stsb-roberta-large')

    # Calculate similarity using Cross encoder
    scores = ce_model.predict(sentence_pairs)

    # Combine the scores with sentence pairs
    combined_scores = list(zip(sentence_pairs, scores))

    # Sort the pairs by Cross Encoder scores
    sorted_pairs = sorted(combined_scores, key=lambda x: x[1], reverse=True)

    # Return the top N pairs and their similarity scores
    top_pairs = sorted_pairs[:top_n]

    return top_pairs

# Example
# sentence_pairs = [
#     ('Dogs are awesome', 'Dogs are special'),
#     ('Popcorn kernels pop in oven', 'There is a sermon on Friday'),
#     ('Some other pair', 'With random content'),
# ]
#
# top_pairs = rerank_query_chunk_pair(sentence_pairs, top_n=3)
# for pair, score in top_pairs:
#     print(f"Pair: {pair}, Score: {score}")