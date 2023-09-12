from typing import List

import numpy as np
import spacy
import math

# Load the Spacy model
nlp = spacy.load('en_core_web_lg')

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

def chunkify(text, degree: float = 45, recursion_level = 1) -> List[str]:
    # Initialize the clusters lengths list and final texts list
    chunks = []

    sentence_clusters = get_sentence_clusters(text, degree)
    for sentence_cluster in sentence_clusters:
        # Check if the cluster is too longs
        if len(sentence_cluster) > 3000 and recursion_level >= 1:
            split_chunks = chunkify(sentence_cluster, degree * 0.5, recursion_level - 1)
            chunks.extend(split_chunks)
        else:
            chunks.append(sentence_cluster)

    return chunks
