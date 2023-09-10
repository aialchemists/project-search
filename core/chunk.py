# pip install numpy spacy
# python -m spacy download en_core_web_sm

import numpy as np
import spacy

# Load the Spacy model
nlp = spacy.load('en_core_web_lg')

def process(text):
    doc = nlp(text)
    sents = list(doc.sents)
    vecs = np.stack([sent.vector / sent.vector_norm for sent in sents])

    return sents, vecs

def cluster_text(sents, vecs, threshold):
    clusters = [[0]]
    for i in range(1, len(sents)):
        if np.dot(vecs[i], vecs[i-1]) < threshold:
            clusters.append([])
        clusters[-1].append(i)

    return clusters

def clean_text(text):
    # Add your text cleaning process here
    return text

def chunkify(text):
    # Initialize the clusters lengths list and final texts list
    chunk_lengths = []
    chunks = []

    # Process the chunk
    threshold = 0.707
    sents, vecs = process(text)

    # Cluster the sentences
    clusters = cluster_text(sents, vecs, threshold)

    for cluster in clusters:
        cluster_txt = clean_text(' '.join([sents[i].text for i in cluster]))
        cluster_len = len(cluster_txt)

        # Check if the cluster is too short
        if cluster_len < 60:
            continue

        # Check if the cluster is too long
        elif cluster_len > 3000:
            threshold = 0.6
            sents_div, vecs_div = process(cluster_txt)
            reclusters = cluster_text(sents_div, vecs_div, threshold)

            for subcluster in reclusters:
                div_txt = clean_text(' '.join([sents_div[i].text for i in subcluster]))
                div_len = len(div_txt)

                if div_len < 60 or div_len > 3000:
                    continue

                chunk_lengths.append(div_len)
                chunks.append(div_txt)

        else:
            chunk_lengths.append(cluster_len)
            chunks.append(cluster_txt)

    return zip(chunks, chunk_lengths)
