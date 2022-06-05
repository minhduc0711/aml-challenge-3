from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
import numpy as np

def get_count_vectorizer(train_tokens):
    # To make CountVectorizer work with tokens: https://stackoverflow.com/a/52855200
    cv = CountVectorizer(tokenizer=lambda x: x, preprocessor=lambda x: x)
    cv.fit(train_tokens)
    
    def transform(tokens):
        return cv.transform([tokens])
    
    return transform

def get_word2vec(tokens, embeddings_index):
    max_tokens = 10
    result = np.zeros((max_tokens, 100))
    if len(tokens) < max_tokens:
        for idx in range(len(tokens)):
            word = tokens[idx]
            try:
                result[idx, :] = embeddings_index[word]
            except:
                continue
    else:
        for idx in range(max_tokens):
            word = tokens[idx]
            try:
                result[idx, :] = embeddings_index[word]
            except:
                continue
    return result.flatten()