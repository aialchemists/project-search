from utils.logger import log

import numpy as np
import spacy
import math

from typing import List, Callable
from utils.configs import chunk_configs

_MODEL_NAME = 'en_core_web_lg'

nlp: Callable

def init():
    log.info(f"Loading Spacy model {_MODEL_NAME}")
    global nlp
    nlp = spacy.load(_MODEL_NAME)
    log.info('Spacy model loaded')

def get_sentences(text):
    doc = nlp(text)
    sents = list(doc.sents)
    vecs = np.stack([sent.vector / sent.vector_norm for sent in sents])

    return sents, vecs

def get_clusters(sents, vecs, threshold):
    clusters = [[0]]
    for i in range(1, len(sents)):
        if np.dot(vecs[i], vecs[i-1]) < threshold:
            clusters.append([])
        clusters[-1].append(i)

    return clusters

def degree_to_threshold(degree:float) -> float:
    radian = degree * math.pi / 180
    threshold = math.cos(radian)
    return threshold

def get_sentence_clusters(text, degree) -> List[str]:
    # Process the chunk
    sents, vecs = get_sentences(text)

    # Cluster the sentences
    threshold = degree_to_threshold(degree)
    clusters = get_clusters(sents, vecs, threshold)

    sentence_clusters = []
    for cluster in clusters:
        sentence_clusters.append(' '.join([sents[i].text for i in cluster]))

    return sentence_clusters

def chunkify(text, degree: float = chunk_configs.degree, recursion_level = 1) -> List[str]:
    # Initialize the clusters lengths list and final texts list
    chunks = []

    sentence_clusters = get_sentence_clusters(text, degree)
    for sentence_cluster in sentence_clusters:
        # Check if the cluster is too longs
        if len(sentence_cluster) > chunk_configs.max_length and recursion_level >= 1:
            split_chunks = chunkify(sentence_cluster, degree * 0.5, recursion_level - 1)
            chunks.extend(split_chunks)
        else:
            chunks.append(sentence_cluster)

    # After all chunks have been added, check and split any chunks that exceed max_length
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > chunk_configs.max_length:
            mid = len(chunk) // 2
            break_at = min(
                chunk.rfind('\n', 0, mid),
                chunk.find('\n', mid),
                key=lambda i: abs(mid - i)  # pick closest to middle
            )
            if break_at > 0:
                firstpart = chunk[:break_at]
                secondpart = chunk[break_at:]
            else:
                firstpart = chunk
                secondpart = ''
            final_chunks.append(firstpart)
            final_chunks.append(secondpart)
        else:
            final_chunks.append(chunk)

    return final_chunks


    # Splitting big chunks midway
    # final_chunks = []
    # for chunk in chunks:
    #     if len(chunk) > chunk_configs.max_length:
    #         # Find the midpoint of the chunk and split it in the middle
    #         midpoint = len(chunk) // 2
    #         final_chunks.append(chunk[:midpoint])
    #         final_chunks.append(chunk[midpoint:])
    #     else:
    #         final_chunks.append(chunk)
    #
    # return final_chunks