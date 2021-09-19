import numpy as np
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from ..common import sentence_similarity
 
def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix



def preprocess(text):
    stop_words = stopwords.words('english')
    try:
        # Step 1 - Read text anc split it
        article = text.split(". ")
        sentences = []

        for sentence in article:
            texts = sentence.replace("[^a-zA-Z]", " ").split(" ")
            texts = [text.replace("\n", "") for text in texts.copy()]
            texts = [text.strip() for text in texts.copy()]
            sentences.append(texts)

        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)
        processed = (sentences, sentence_similarity_martix)

        error = False
    except Exception:
        error = True

    return error, processed

