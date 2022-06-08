import contractions
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import names
from textacy import preprocessing
import string
import emot

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('names', quiet=True)

lemmatizer = WordNetLemmatizer()
stops = set(stopwords.words("english"))
stops.remove("can")
stops.remove("not")
stops.remove("won")

human_names = set(names.words("male.txt") + names.words("female.txt"))
human_names.remove("Happy")


vocab_emoji = {
    ';)': 'smirk',
    ':]': 'smiley',
    ':/': 'skeptical',
    'd:': 'cheeky',
    ':@': 'sad',
    '=/': 'annoyed',
    ':|': 'neutral',
    '=]': 'happy',
    ':>': 'happy',
    ':o': 'surprise',
    ':$': 'blushing',
    '=p': 'cheeky',
    ':[': 'sad',
    '8-)': 'happy',
    ':*': 'kiss',
    ':-0': 'shock',
    ":'(": 'crying',
    ":b": 'cheeky',
    ":{": 'sad',
    ":')": 'sad',
    ':x': 'mute',
    ':-*': 'kiss',
}
emot_obj = emot.core.emot()

def preprocess(text):
    text = preprocessing.replace.urls(text, "")
    text = re.sub('\d+:\d+', '', text) # remove time
    
    text = preprocessing.normalize.quotation_marks(text)
    # Resolve contractions & slangs
    text = contractions.fix(text, slang=True)
    # Remove username handles
    text = re.sub(r"@[^\s]+", "", text)
    text = re.sub(r"_[^\s]+", "", text)
    
    # Emoticons
    # TODO: censored curse words ****
    text = re.sub(r"<3+", " love", text)
    
    text = preprocessing.replace.numbers(text, "")

    text = text.translate(str.maketrans({key: " " for key in string.punctuation}))
    text = preprocessing.normalize.whitespace(text)
    
    # TODO: filter out names & certain stopwords
    # TODO: ugly to tokenize in the preprocess fn..
    # tokens = word_tokenize(text)
    # tokens = [token for token in tokens if token not in human_names]
    # tokens = [token for token in tokens if token.lower() not in stops]
    # tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # text = " ".join(tokens)
    
    text = text.lower()
    return text

def fix_emoji(text):
    emojis = emot_obj.emoticons(text)
    for value in emojis['value']:
        if value in vocab_emoji:
            text = text.replace(value, vocab_emoji[value])
        else:
            continue
    return text