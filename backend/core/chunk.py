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

def get_group(sents, vecs, threshold):
    group = [[0]]
    for i in range(1, len(sents)):
        if np.dot(vecs[i], vecs[i-1]) < threshold:
            group.append([])
        group[-1].append(i)

    return group

def degree_to_threshold(degree:float) -> float:
    radian = degree * math.pi / 180
    threshold = math.cos(radian)
    return threshold

def get_sentence_group(text, degree) -> List[str]:
    # Process the chunk
    sents, vecs = get_sentences(text)

    # Cluster the sentences
    threshold = degree_to_threshold(degree)
    group = get_group(sents, vecs, threshold)

    sentence_group = []
    for cluster in group:
        sentence_group.append(' '.join([sents[i].text for i in cluster]))

    return sentence_group

def divide_larger_chunks(text, piece_length):
    # Initialize an empty list to store the divided pieces
    divided_pieces = []

    # Loop through the input_string in steps of piece_length
    for i in range(0, len(text), piece_length):
        # Extract a piece of the specified length
        piece = text[i:i + piece_length]
        divided_pieces.append(piece)

    return divided_pieces


def chunkify(text, degree: float = chunk_configs.degree, recursion_level = 1) -> List[str]:
    # Initialize the group lengths list and final texts list
    chunks = []

    sentence_group = get_sentence_group(text, degree)
    for sentence_cluster in sentence_group:
        # Check if the cluster is too longs
        if len(sentence_cluster) > chunk_configs.max_length and recursion_level >= 1:
            split_chunks = chunkify(sentence_cluster, degree * 0.5, recursion_level - 1)
            chunks.extend(split_chunks)
        else:
            chunks.append(sentence_cluster)

    final_chunks = []
    for chunk in chunks:
        if len(chunk) > chunk_configs.max_length:
            divided_chunks = divide_larger_chunks(chunk, chunk_configs.max_length)
            final_chunks.extend(divided_chunks)  # Append the divided chunks to the final_chunks list
        else:
            final_chunks.append(chunk)

    return final_chunks
