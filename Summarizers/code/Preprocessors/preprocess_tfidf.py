from nltk.tokenize import sent_tokenize
from spacy.lang.en import English

def preprocess(text):
    try:
        nlp = English()
        nlp.create_pipe('sentencizer')
        tokenizer = sent_tokenize
        doc = nlp(text.replace('\n', ''))
        doc = tokenizer(str(doc))
        sentences = [sent.strip() for sent in doc]
        max_sents = len(sentences) // 5
        text = [sentences, max_sents]
        error = False
    except Exception:
        error = True
    return error, text
