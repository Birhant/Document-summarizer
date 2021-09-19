import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def summarize(text):
    sentences, freqTable, percent = text

    sentenceValue = dict()
    for sentence in sentences:
        for word,freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence]+=freq
                else:
                    sentenceValue[sentence]=freq
    max_freq = 0
    for sentence in sentenceValue:
        max_freq = max(max_freq, sentenceValue[sentence])

    summary=''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence]>=(percent * max_freq)):
            summary+=" "+sentence
    return summary

