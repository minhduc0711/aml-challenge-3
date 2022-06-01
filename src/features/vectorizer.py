from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize

def get_count_vectorizer(train_tokens):
    # To make CountVectorizer work with tokens: https://stackoverflow.com/a/52855200
    cv = CountVectorizer(tokenizer=lambda x: x, preprocessor=lambda x: x)
    cv.fit(train_tokens)
    
    def transform(tokens):
        return cv.transform([tokens])
    
    return transform