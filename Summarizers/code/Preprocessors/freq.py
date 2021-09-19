import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def preprocess(text, percent = 0.8):
    error = True

    stopword = set(stopwords.words("english"))
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    if(len(words)<10 or len(sentences)<2):
        a=10
    else:
        freqTable = dict()
        for word in words:
            word=word.lower()
            if word in stopword:
                continue
            if word in freqTable:
                freqTable[word]+=1
            else:
                freqTable[word]=1
        error = False
        text = (sentences, freqTable, percent)

    if type(percent)==type('int'):
        if percent<1.0 and percent>0:
            error = True

    return error, text

