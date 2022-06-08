import contractions
import re
import emot
from textacy.preprocessing.normalize import quotation_marks

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

misspelling = {
    'bday': 'birthday',
    'itll': 'it will',
    'youve': 'you have',
    'idk': 'i do not know',
    'followfriday': 'follow friday',
    'shouldnt': 'should not',
    'tonights': 'tonight',
    'sux': 'suck',
    'mommys': 'mommy',
    'werent': 'were not',
    'everyones': 'everyone',
    'theyve': 'they have',
    'lmao': 'haha',
    'LMAO': 'haha',
    'awsome': 'awesome',
}

emot_obj = emot.core.emot()

def preprocess(text):
    # text = text.lower()
    text = remove_url(text)
    text = re.sub('\d+:\d+', '', text) # remove time
    text = fix_emoji(text)
    text = re.sub('<3+', 'love', text)
    # text = fix_contractions_slang(text)
    # text = remove_punctuation(text)
    # text = fix_laughing_words(text)
    # text = fix_misspelling_word(text)

    return text

def fix_contractions_slang(text):
    text = quotation_marks(text) # Fix quotations mark
    text = contractions.fix(text)
    return text

def fix_heart(x):
    x = re.sub('<3+', 'love', x)
    return x

def remove_time(time):
    time = re.sub('\d+:\d+', '', time)
    return time

def fix_emoji(text):
    emojis = emot_obj.emoticons(text)
    for value in emojis['value']:
        if value in vocab_emoji:
            text = text.replace(value, vocab_emoji[value])
        else:
            continue
    return text

def remove_url(text):
    return re.sub(r'http\S+', '', text)

def remove_punctuation(text):
    text = str(text)
    for punct in "/-'":
        text = text.replace(punct, ' ')
    for punct in '&':
        text = text.replace(punct, f' {punct} ')
    for punct in '?!.,"#$%\'()*+-/:;<=>@[\\]^_`{|}~' + '“”’':
        text = text.replace(punct, '')
    return text

# Need to improve this function
def fix_laughing_words(x):
    # Change hahahahaha or lolololo to haha
    return re.sub(r'\b(?:a*(?:ha)+h?|(?:l+o+)+l+)\b', 'haha', x)

# Fix soooooo to so and Lmao
def fix_misspelling_word(x):
    # fix soooooo to so    
    x = re.sub(r'\b(?:s+o+)+\b', 'so', x)
    for word in x.split():
        if word in misspelling.keys():
            x = x.replace(word, misspelling[word])
    return x