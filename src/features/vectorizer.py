import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import gensim.downloader as api
from nltk.tokenize import word_tokenize

def get_count_vectorizer(train_tokens):
    # To make CountVectorizer work with tokens: https://stackoverflow.com/a/52855200
    cv = CountVectorizer(tokenizer=lambda x: x, preprocessor=lambda x: x)
    cv.fit(train_tokens)

    def transform(tokens):
        return cv.transform([tokens])

    return transform

def get_glove_vectorizer(maxlen):
    print("Loading pretrained Glove")
    wv = api.load('glove-twitter-200')
    print("Done")

    def transform(tokens):
        x = []
        for token in tokens:
            if token in wv:
                x.append(wv[token])
            else:
                # TODO: might dilute the representation
                x.append(np.zeros(200))
        x = np.vstack(x)
        if maxlen != -1:
            if x.shape[0] < maxlen:
                pad = np.zeros((maxlen - x.shape[0], x.shape[1]))
                x = np.concatenate((x, pad))
            elif x.shape[1] > maxlen:
                x = x[:maxlen, :]
        return x


    return transform
