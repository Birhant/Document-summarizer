from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer


def preprocess(text):
    try:
        my_parser = PlaintextParser.from_string(text, Tokenizer('english'))
        error = False
    except Exception:
        error = True
    return error, my_parser



