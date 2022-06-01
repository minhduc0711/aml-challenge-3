import contractions

def preprocess(text):
    text = text.lower()
    # Resolve contractions & slangs
    text = contractions.fix(text)
    
    return text
